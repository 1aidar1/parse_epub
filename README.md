
``` mermaid
sequenceDiagram;

    Client->>App: Do my task!
    App->> ClientTarget: Do.
    ClientTarget->> App: Fail. Code:>400.
    App->> Rabbit: Queue task with delay.
    Rabbit->> App: Delay ended.
    App->> ClientTarget: Do.
    ClientTarget->> App: Success or No More Tries.
    App->> Client: callback.


```
