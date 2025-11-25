import grpc
import generalAPI_pb2_grpc as pb2_grpc
import generalAPI_pb2 as pb2
import json
import logging
import os
from pathlib import Path
base_path = Path(__file__).parent
CHUNK_SIZE = 20 * 1024 * 1024


def upload_file_to_server(stub, file_path, filename):
    def generate_chunks():
        with open(file_path, 'rb') as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                yield pb2.client_upload_request(filename=filename, data=chunk)

    try:
        response = stub.client_upload_file(generate_chunks())
        if response.success:
            logging.info(response.message)
            return True
        else:
            logging.error(response.message)
            return False
    except Exception as e:
        logging.error(f"Error uploading file {filename}: {str(e)}")
        return False


def upload_directory_to_server(stub, dir_path):
    """上传整个目录中的所有文件到服务器"""
    uploaded_files = []

    if not dir_path.is_dir():
        logging.error(f"Path is not a directory: {dir_path}")
        return []

    for file_path in dir_path.iterdir():
        if file_path.is_file():
            filename = file_path.name
            logging.info(f"Uploading file: {file_path} as {filename}")

            if upload_file_to_server(stub, file_path, filename):
                uploaded_files.append(filename)
            else:
                logging.error(f"Failed to upload file: {file_path}")
                return []  # 如果任何文件上传失败，返回空列表

    return uploaded_files

def run(config):

    parameters = config["parameters"]
    inputs = config["inputs"]
    outputs = config["outputs"]
    model_flag = config["model_flag"]

    channel = grpc.insecure_channel('localhost:7070')
    stub = pb2_grpc.generalAPIStub(channel)

    uploaded_files = {}
    if inputs and "data_set_path" in inputs:
        local_path = base_path / inputs["data_set_path"]

        if local_path.is_dir():
            # 如果是目录，上传目录中的所有文件
            logging.info(f"Uploading directory: {local_path}")
            uploaded_file_list = upload_directory_to_server(stub, local_path)

            if uploaded_file_list:
                uploaded_files[inputs["data_set_path"]] = uploaded_file_list
                # 路径修改为服务器端的inputs目录
                inputs["data_set_path"] = "inputs"
            else:
                logging.error(f"Failed to upload directory: {local_path}")
                channel.close()
                return json.dumps({"error": "Directory upload failed"})

        elif local_path.is_file():
            # 如果是单个文件，使用原有逻辑
            filename = local_path.name
            logging.info(f"Uploading file: {local_path} as {filename}")

            if upload_file_to_server(stub, local_path, filename):
                uploaded_files[inputs["data_set_path"]] = filename
                # 路径修改，server端存储为inputs/filename
                inputs["data_set_path"] = f"inputs/{filename}"
            else:
                logging.error(f"Failed to upload file: {local_path}")
                channel.close()
                return json.dumps({"error": "File upload failed"})
        else:
            logging.error(f"Local path not found: {local_path}")
            channel.close()
            return json.dumps({"error": f"Local path not found: {local_path}"})

    response = stub.remote_call(
        pb2.general_request(
            parameters=json.dumps(parameters),
            inputs=json.dumps(inputs),
            outputs=json.dumps(outputs),
            model_flag=json.dumps(model_flag)
        )
    )
    files_on_client = []

    if response.upload_or_not is True:

        # TODO:路径修改
        new_results_dir = base_path / "results"
        os.makedirs(new_results_dir, exist_ok=True)

        for filename in outputs["filenames"]:
            r = pb2.upload_request(filename=filename)
            flow = stub.upload_file(r)
            file_path_on_client = new_results_dir / filename
            files_on_client.append(str(file_path_on_client))
            with open(file_path_on_client, 'wb') as f:
                for r in flow:
                    f.write(r.data)

    channel.close()

    final_outputs = {}
    final_outputs["Model"] = str(response.model_description)
    json_output_data = json.loads(response.json_output)
    final_outputs.update(json_output_data)
    final_outputs["Client_File_Path"] = files_on_client

    outputs_json = json.dumps(final_outputs, indent=4, ensure_ascii=False)
    logging.info(f"Outputs: {outputs_json}")
    return outputs_json

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(filename)s] => %(message)s")
    with open("configs/config.json", 'r') as f:
        config = json.load(f)
    run(config)
