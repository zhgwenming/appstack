#!/usr/bin/env escript
-export([main/1]).

unpack_data(Bin) ->
    <<Version:32/native,
      StructSize:32/native,
      CPULocalMS:64/native,
      CPUIdleMS:64/native,
      SwapTotal:64/native,
      SwapUsed:64/native,
      SwapPageIn:64/native,
      SwapPageOut:64/native,
      MemTotal:64/native,
      MemUsed:64/native,
      MemActualUsed:64/native,
      MemActualFree:64/native>> = Bin,
    StructSize = erlang:size(Bin),
    Version = 0,
    [{cpu_local_ms, CPULocalMS},
     {cpu_idle_ms, CPUIdleMS},
     {swap_total, SwapTotal},
     {swap_used, SwapUsed},
     {swap_page_in, SwapPageIn},
     {swap_page_out, SwapPageOut},
     {mem_total, MemTotal},
     {mem_used, MemUsed},
     {mem_actual_used, MemActualUsed},
     {mem_actual_free, MemActualFree}].

main([]) ->
    Port = open_port({spawn_executable, "./sigar_port"},
                     [stream, use_stdio, exit_status,
                      binary, eof, {arg0, "no cigar for alk:)"}]),

    port_command(Port, <<0:32/native>>),

    receive
        {Port, {data, Data}} ->
            io:format("~p~n", [unpack_data(Data)]);
        X ->
            io:format("unexpected: ~p~n", [X])
    end.
