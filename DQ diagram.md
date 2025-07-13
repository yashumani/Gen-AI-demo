'''mermaid 
sequenceDiagram
    autonumber
    participant SQL_DB
    participant KNIME_Server
    participant NetShare as "Shared Folder\n(\\\\fileshare\\watchdog_inbox)"
    participant Watchdog as "Watchdog\n(Local PC)"
    participant Vertex
    participant You as "You\n(UI)"

    SQL_DB-->>KNIME_Server: Query result set
    KNIME_Server->>NetShare: Create Temp Dir + export.csv
    Note right of KNIME_Server: No REST • No shell<br>Only file I/O
    NetShare-->>Watchdog: Filesystem “CREATE” event
    Watchdog->>Watchdog: Load file → run DQ rules
    Watchdog->>Vertex: POST predict(prompt_json)
    Vertex-->>Watchdog: Markdown narrative
    Watchdog-->>You: Stream card via WebSocket
    You-->>Watchdog: (optional) Thumbs-up/down feedback