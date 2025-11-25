import grpc
import generalAPI_pb2_grpc as pb2_grpc
import generalAPI_pb2 as pb2
import json

json_input = {"q0": 18.529 * 3.1415926 / 180, "q1": -17.071 * 3.1415926 / 180, "v0": 0, "v1": 0, "vmax": 0.2,
              "amax": 0.5, "jmax": 1}
data_set = 'None'
obj_set = "None"
model_flag = {"result_output_path": "D:\\FinalSeal\\result\\", "result_output_name": "Trajectory000.jpg"}
json_input = json.dumps(json_input)
model_flag = json.dumps(model_flag)


def run():
    channel = grpc.insecure_channel('localhost:7070')
    stub = pb2_grpc.generalAPIStub(channel)

    response = stub.remote_call(
        pb2.general_request(
            json_input=json_input,
            data_set=data_set,
            obj_set=obj_set,
            model_flag=model_flag
        )
    )
    print("Result 1:", response.json_output)
    print("Result 2:", response.string_output1)
    print("Result 3:", response.string_output2)
    print("Result 4:", response.string_output3)
    channel.close()


if __name__ == '__main__':
    run()
