clear;
close all;

fprintf('Creating server socket...');
TCPIPServer = tcpserver('127.0.0.1', 6001);
fprintf(' CREATED\n');
while true
    if TCPIPServer.NumBytesAvailable ~= 0
        data = read(TCPIPServer, TCPIPServer.NumBytesAvailable, "string");
        reply(TCPIPServer,data)
    end
end    

function reply(srv, packet)
    while (1) % try a few times, if you only try once you get an error saying client is not connected
        try
            disp(packet);
            srv.write(packet+ " Hello"); % send reply to proxy        
            break;
        catch
            pause(0.01); % wait for some amount
        end
    end
end