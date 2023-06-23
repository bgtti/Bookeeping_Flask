from datetime import datetime

ExpensesData = [
    {
        "id": 'ex1',
        "exDate": datetime.strptime("2023-01-01 00:10:00", '%Y-%m-%d %H:%M:%S'),
        "exNr": "22-10-001",
        "exDescription": "Electricity bill",
        "exAmount": 200.00,
        "project": "Project 1",
        "type": "Utilities",
        "account": "Bank",
    },
    {
        "id": 'ex2',
        "exDate": datetime.strptime("2023-01-01 00:10:00", '%Y-%m-%d %H:%M:%S'),
        "exNr": "22-10-002",
        "exDescription": "Electricity bill",
        "exAmount": 200.00,
        "project": "Project 1",
        "type": "Utilities",
        "account": "Bank",
    },
    {
        "id": 'ex3',
        "exDate": datetime.strptime("2023-01-01 00:10:00", '%Y-%m-%d %H:%M:%S'),
        "exNr": "22-10-003",
        "exDescription": "Water bill",
        "exAmount": 200.00,
        "project": "Project 1",
        "type": "Utilities",
        "account": "Cash",
    },
    {
        "id": 'ex4',
        "exDate": datetime.strptime("2023-01-01 00:10:00", '%Y-%m-%d %H:%M:%S'),
        "exNr": "22-09-001",
        "exDescription": "Internet bill",
        "exAmount": 200.00,
        "project": "Project 1",
        "type": "Utilities",
        "account": "Cash",
    },
]
