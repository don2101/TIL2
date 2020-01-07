class StatusCheck:
    _instance = None
    _servers = []
    
    def __new__(cls, *args, **kwargs):
        if not StatusCheck._instance:
            StatusCheck._instance = super(StatusCheck, cls).__new__(cls, *args, **kwargs)

        return StatusCheck._instance

    def __init__(self):
        self._servers = []

    def addServer(self):
        self._servers.append("Server 1")
        self._servers.append("Server 2")
        self._servers.append("Server 3")
        self._servers.append("Server 4")

    def changeServer(self):
        self._servers.pop()
        self._servers.append("Server 5")


status_check1 = StatusCheck()
status_check2 = StatusCheck()

status_check1.addServer()
print("Schedule statue check for servers (1)")

for i in range(4):
    print("Checking ", status_check1._servers[i])

status_check2.changeServer()
print("Schedule statue check for servers (2)")

for i in range(4):
    print("Checking ", status_check2._servers[i])
