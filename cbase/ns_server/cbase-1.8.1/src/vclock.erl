%% @copyright 2007-2008 Basho Technologies

%% @reference Leslie Lamport (1978). "Time, clocks, and the ordering of events in a distributed system". Communications of the ACM 21 (7): 558-565.

%% @reference Friedemann Mattern (1988). "Virtual Time and Global States of Distributed Systems". Workshop on Parallel and Distributed Algorithms: pp. 215-226

%% @author Justin Sheehy <justin@basho.com>
%% @author Andy Gross <andy@basho.com>

%% @doc A simple Erlang implementation of vector clocks as inspired by Lamport logical clocks.

%% Copyright 2007-2008 Basho Technologies

%% Licensed under the Apache License, Version 2.0 (the "License");
%% you may not use this file except in compliance with the License.
%% You may obtain a copy of the License at

%% http://www.apache.org/licenses/LICENSE-2.0

%% Unless required by applicable law or agreed to in writing, software
%% distributed under the License is distributed on an "AS IS" BASIS,
%% WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
%% See the License for the specific language governing permissions and
%% limitations under the License.

-module(vclock).

-author('Justin Sheehy <justin@basho.com>').
-author('Andy Gross <andy@basho.com>').

-export([fresh/0,descends/2,merge/1,get_counter/2,get_timestamp/2,
         increment/2,all_nodes/1, likely_newer/2]).
-export([example_test/0]).

% @type vclock() = [vc_entry].
% @type   vc_entry() = {node(), {counter(), timestamp()}}.
% The timestamp is present but not used, in case a client wishes to inspect it.
% @type   node() = term().
% Nodes can have any term() as a name, but they must differ from each other.
% @type   counter() = integer().
% @type   timestamp() = integer().

% @doc Create a brand new vclock.
% @spec fresh() -> vclock()
fresh() ->
    [].

% @doc Reflect an update performed by Node.
%      See increment/2 for usage.
% @spec extend(VC_Entry :: VC_Entry, VClock :: vclock()) -> vclock()
extend({Node,{Ctr,TS}}, VClock) ->
    simplify([{Node,{Ctr,TS}}|VClock]).

% @doc Remove trivial ancestors.
% @spec simplify(vclock()) -> vclock()
simplify(VClock) ->
    simplify(VClock, []).
simplify([], NClock) ->
    NClock;
simplify([{Node,{Ctr1,TS1}}|VClock], NClock) ->
    {Ctr2,TS2} = proplists:get_value(Node, NClock, {Ctr1,TS1}),
    {Ctr,TS} = if
                   Ctr1 > Ctr2 ->
                       {Ctr1,TS1};
                   true ->
                       {Ctr2,TS2}
               end,
    simplify(VClock, [{Node,{Ctr,TS}}|proplists:delete(Node, NClock)]).

%% @todo Use common_test or other good test framework, and write more tests.
%
% @doc Serves as both a trivial test and some example code.
example_test() ->
    A = vclock:fresh(),
    B = vclock:fresh(),
    A1 = vclock:increment(a, A),
    B1 = vclock:increment(b, B),
    true = vclock:descends(A1,A),
    true = vclock:descends(B1,B),
    false = vclock:descends(A1,B1),
    A2 = vclock:increment(a, A1),
    C = vclock:merge([A2, B1]),
    C1 = vclock:increment(c, C),
    true = vclock:descends(C1, A2),
    true = vclock:descends(C1, B1),
    false = vclock:descends(B1, C1),
    false = vclock:descends(B1, A1),
    BadClock1 = [{node1, {1, 10}}, {node2, {1, 20}}],
    BadClock2 = [{node1, {1, 12}}, {node2, {1, 20}}],
    true = vclock:descends(BadClock1, BadClock2),
    true = vclock:descends(BadClock2, BadClock1),
    false = vclock:likely_newer(BadClock1, BadClock2),
    true = vclock:likely_newer(BadClock2, BadClock1),
    BadClock3 = [{node1, {1, 12}}, {node2, {1, 21}}],
    true = vclock:descends(BadClock1, BadClock3),
    true = vclock:descends(BadClock3, BadClock1),
    false = vclock:likely_newer(BadClock1, BadClock3),
    true = vclock:likely_newer(BadClock3, BadClock1),
    ok.

% @doc Return true if Va is a direct descendant of Vb, else false -- remember, a vclock is its own descendant!
% @spec descends(Va :: vclock(), Vb :: vclock()) -> bool()
descends(_, []) ->
    % all vclocks descend from the empty vclock
    true;
descends(Va, Vb) ->
    [{NodeB, {CtrB, _T}}|RestB] = Vb,
    CtrA =
        case proplists:get_value(NodeB, Va) of
            undefined ->
                false;
            {CA, _TSA} -> CA
        end,
    case CtrA of
        false -> false;
        _ ->
            if
                CtrA < CtrB ->
                    false;
                true ->
                    descends(Va,RestB)
            end
    end.

%% @doc Applies to case where descends(Va, Vb) is true and
%% descends(Vb, Va) is true. Returns true iff Va has later timestamp
%% then Vb for one of the nodes.
likely_newer(Va, Vb) ->
    lists:any(fun ({Node, {_Counter, TStampA}}) ->
                      case lists:keyfind(Node, 1, Vb) of
                          false -> false;
                          {_, {_CounterB, TStampB}} ->
                              TStampA > TStampB
                      end
              end, Va).

% @doc Combine all VClocks in the input list into their least possible
%      common descendant.
% @spec merge(VClocks :: [vclock()]) -> vclock()
merge(VClocks) ->
    merge(VClocks, []).
merge([], NClock) ->
    NClock;
merge([AClock|VClocks],NClock) ->
    merge(VClocks, lists:foldl(fun(X,L) -> extend(X,L) end, NClock, AClock)).

% @doc Get the counter value in VClock set from Node.
% @spec get_counter(Node :: node(), VClock :: vclock()) -> counter()
get_counter(Node, VClock) ->
    case proplists:get_value(Node, VClock) of
        {Ctr, _TS} -> Ctr;
        undefined -> undefined
    end.

% @doc Get the timestamp value in a VClock set from Node.
% @spec get_timestamp(Node :: node(), VClock :: vclock()) -> timestamp()
get_timestamp(Node, VClock) ->
    case proplists:get_value(Node, VClock) of
        {_Ctr, TS} -> TS;
        undefined -> undefined
    end.

% @doc Increment VClock at Node.
% @spec increment(Node :: node(), VClock :: vclock()) -> vclock()
increment(Node, VClock) ->
    {Ctr, TS} = case proplists:get_value(Node, VClock) of
                    undefined ->
                        {1, timestamp()};
                    {C, _T} ->
                        {C + 1, timestamp()}
                end,
    extend({Node, {Ctr, TS}}, VClock).

% @doc Return the list of all nodes that have ever incremented VClock.
% @spec all_nodes(VClock :: vclock()) -> [node()]
all_nodes(VClock) ->
    [X || {X,{_,_}} <- VClock].

timestamp() ->
    calendar:datetime_to_gregorian_seconds(erlang:universaltime()).
