import time
import json
import grpc
import generalAPI_pb2_grpc as pb2_grpc
import generalAPI_pb2 as pb2
from Trajectory import Trajectory
from concurrent import futures
from pathlib import Path
import logging

CHUNK_SIZE = 4 * 1024 * 1024
base_path = Path(__file__).parent

def file_read(filename):

    file_path = base_path / "result" / filename

    logging.info(f"Attempting to upload file in server: {file_path}")

    with open(file_path, "rb") as file:
        start = 0
        while True:
            file.seek(start)
            read = file.read(CHUNK_SIZE)
            if not read:
                return
            yield pb2.upload_response(data=read)
            start += CHUNK_SIZE

class trajectory_server(pb2_grpc.generalAPIServicer):
    def remote_call(self, request, context):
        parameters = request.parameters
        inputs = request.inputs
        outputs = request.outputs
        model_flag = request.model_flag
        try:
            parameters = json.loads(parameters)
            inputs = json.loads(inputs)
            outputs = json.loads(outputs)
            model_flag = json.loads(model_flag)
            q0 = inputs["q0"]
            q1 = inputs["q1"]
            v0 = inputs["v0"]
            v1 = inputs["v1"]
            vmax = inputs["vmax"]
            amax = inputs["amax"]
            jmax = inputs["jmax"]
            path = outputs["path"]
            name = outputs["filenames"][0]

            result = Trajectory(q0, q1, v0, v1, vmax, amax, jmax, path, name)
            json_output = json.dumps({"results": result})

            if outputs["path"] is not None:
                upload_or_not = True
            else:
                upload_or_not = False

        except Exception as e:
            raise ValueError(str(e))

        return pb2.general_response(
            json_output=json_output,
            model_description=model_flag,
            upload_or_not=upload_or_not
        )
    def upload_file(self, request, context):
        filename = request.filename
        file = file_read(filename)
        for response in file:
            yield response

    def client_upload_file(self, request_iterator, context):
        try:
            uploaded_dir = base_path / "inputs"
            uploaded_dir.mkdir(exist_ok=True)

            filename = None
            file_path = None

            for request in request_iterator:
                if filename is None:
                    filename = request.filename
                    file_path = uploaded_dir / filename
                    logging.info(f"Receiving file: {filename}")

                # 写入文件数据
                with open(file_path, 'ab') as f:
                    f.write(request.data)

            if filename:
                logging.info(f"File {filename} uploaded successfully to {file_path}")
                return pb2.client_upload_response(
                    success=True,
                    message=f"File {filename} uploaded successfully"
                )
            else:
                return pb2.client_upload_response(
                    success=False,
                    message="No file data received"
                )

        except Exception as e:
            logging.error(f"Error receiving file: {str(e)}")
            return pb2.client_upload_response(
                success=False,
                message=f"Error uploading file: {str(e)}"
            )
def run():
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_generalAPIServicer_to_server(trajectory_server(), server)
    server.add_insecure_port('0.0.0.0:7070')
    logging.info("Server in 0.0.0.0:7070")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(filename)s] => %(message)s")
    run()


