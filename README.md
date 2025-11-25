Outputs: {
    "Model": "7070",
    "results": {
        "plot_name": "./result/trajectory.jpg"
    },
    "Client_File_Path": [
        "D:\\Pythonproject\\fengzhuang\\S_Trajectory_grpc\\results\\trajectory.jpg"
    ]
}

使用grpc框架实现客户端和服务端的双向通信。
generalAPI.proto中定义了三种主要的RPC服务：
service generalAPI{
  rpc remote_call(general_request) returns(general_response);  // 双向单次调用
  rpc upload_file(upload_request) returns(stream upload_response);  // 服务端到客户端流
  rpc client_upload_file(stream client_upload_request) returns(client_upload_response);  // 客户端到服务端流
}
客户端发起计算请求，请求内容在general_raquest中定义。
string parameters = 1;   // JSON 字符串
string inputs      = 2;   // JSON 字符串，q0, q1... 
string outputs     = 3;   // JSON 字符串，path, filenames
string model_flag  = 4;   // 字符串
服务端解析json，调用主函数，并将结果保存到./result/trajectory.jpg，返回general_response
string json_output       = 1;  // 计算结果（JSON）
string model_description = 2;  // model_flag 回传
bool   upload_or_not     = 3;  // 是否有文件需下载
客户端下载结果文件：response.upload_or_not == True
客户端发送文件名(filename="trajectory.jpg")，服务端打开./result/trajectory.jpg
客户端写入本地./results/