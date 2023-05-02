clear;
close all;

fprintf('Creating server socket...');
TCPIPServer = tcpserver('127.0.0.1', 6002);
fprintf(' CREATED\n');
serverData = cell(1,10);

while true
    if TCPIPServer.NumBytesAvailable ~= 0
        data = read(TCPIPServer, TCPIPServer.NumBytesAvailable, "string");
        reply(TCPIPServer,data)
    end
end    

function reply(srv, packet)
    persistent serverData
    if isempty(serverData)
        serverData = cell(1,10);
    end
    
    while (1)
        try
            disp(packet);
            opcodeData = split(packet, ':');
            opcode = opcodeData{1};
            
            switch opcode
                case "GET"
                    index = str2double(opcodeData{2});
                    dataToSend = serverData{index+1};
                    fprintf("Decoded OP: GET--> ID: %d DATA: %d\n", index, dataToSend);
                case "PUT"
                    index = str2double(opcodeData{2});
                    data = str2double(opcodeData{3});
                    serverData{index+1} = data;
                    dataToSend = serverData{index+1};
                    fprintf("Decoded OP: PUT--> ID: %d DATA: %d\n", index, dataToSend);
                case "CLR"
                    serverData = cell(1,10);
                    dataToSend = "-";
                    fprintf("Decoded OP: CLR--> DATA: %s\n", dataToSend);
                case "ADD"
                    index = str2double(opcodeData{2});
                    dataToSend = serverData{index+1};
                    fprintf("Decoded OP: ADD--> ID: %d DATA: %d\n", index, dataToSend);
            end

            fprintf("Remote Server Data by Order: ");
            for i = 1:numel(serverData)
                fprintf("%d ", serverData{i});
            end
            fprintf("\n");

            srv.write(num2str(dataToSend)); % send reply to proxy
            break;
        catch
            pause(0.01); % wait for some amount
        end
    end
end
