import time
import json
import grpc
import generalAPI_pb2_grpc as pb2_grpc
import generalAPI_pb2 as pb2
from concurrent import futures
from Trajectory import Trajectory


class trajectory_server(pb2_grpc.generalAPIServicer):
    def remote_call(self, request, context):
        json_input = request.json_input
        data_set = request.data_set
        obj_set = request.obj_set
        model_flag = request.model_flag
        try:
            json_input = json.loads(json_input)
            model_flag = json.loads(model_flag)
            q0 = json_input["q0"]
            q1 = json_input["q1"]
            v0 = json_input["v0"]
            v1 = json_input["v1"]
            vmax = json_input["vmax"]
            amax = json_input["amax"]
            jamx = json_input["jmax"]
            path = model_flag["result_output_path"]
            name = model_flag["result_output_name"]

            result = Trajectory(q0, q1, v0, v1, vmax, amax, jamx, path, name)
            json_output = json.dumps(result)
            string_output1 = "trajectory_string_output1"
            string_output2 = "trajectory_string_output2"
            string_output3 = "trajectory_string_output3"
        except Exception as e:
            print(e)
            json_output = json.dumps({"key": "trajectory_json_output"})
            string_output1 = "trajectory_string_output1"
            string_output2 = "trajectory_string_output2"
            string_output3 = "trajectory_string_output3"
        return pb2.general_response(
            json_output=json_output,
            string_output1=string_output1,
            string_output2=string_output2,
            string_output3=string_output3
        )


def run():
    server = grpc.server(thread_pool=futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_generalAPIServicer_to_server(trajectory_server(), server)
    server.add_insecure_port('0.0.0.0:7070')
    server.start()
    print('server start at 0.0.0.0:7070')
    try:
        while 1:
            time.sleep(1)
    except KeyboardInterrupt:
        server.stop(0)
        print('server stopped')


if __name__ == '__main__':
    run()

