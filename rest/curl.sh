curl -m 1 -L -g 'http://192.168.15.58:1234/api/MissionCreate?access_token=AQAAANCMnd8BFdERjHoAwE_Cl-sBAAAAdvQ1hwE1kEOaRn4wCDHVHQAAAAACAAAAAAAQZgAAAAEAACAAAADeWKLvmFi5q6FOtj7VOuoYWNnsvGWSyMD_S-9OFzI77QAAAAAOgAAAAAIAACAAAABXZecucyDjuC-anhnZSHWR9KgLraGewx2saSa93_PS5eACAAAJtZv5etLLzUlmbndIh_kfZ5KW3ycR5n-rvcXxQ9BgEfldDUijOzMrGK7qWcqcyYKRa9W66ZnvNuZb7kd9gjXr1esUbQ-22AyE4kh1XwkS409Byx8hB-nesPX_eTD_zFQH8zABzLW2aQlnAWVH1OSvkaonjar_WmPHXcYvVR8NGvCaguK-eEkVnnBtqaMeiDic69YQvSQDQ3AlKp0tbfvI7G60plBtP_JdtaqBWM1gl2EWe8OnwlbLayi0yoDkZoee-f482VdLy3iIo0XI_6DyrxH6b1rtvWw7aEjVON86-czCEGgMAOzdmXvgFo-6xcMZHG7YZUADuY5OVjOQ1vmpO6VUxntNH7qHO41Nf8JYJDLtukBNR3rQDSq5e10tVNPNUFNpwI6B3vgsp-pHwOJUtvg6YsIDfQgWJHqSWRzNeUcthPy2LP19KlfI94SSETHZQxIAWpSlxlycWY-MUgn3ojAFWfLHQH8L1GDp6UW-EQ4pcALDFcagFVHFwAzaMIw-wlZ1RsYdVSOQUYfHl79uivbWyxY1QCUv_yb8S7qqsOvshNbhLfBP9rnnbJujMcT7EoEoNjyR9i3SCxU7UbQUgCYWyBP13Xkh8_Ey7HI17JsinvhpznWjWx7-jmsJMB8qpc8LvKJZC8Y-TvCAgVv3gEwSdThn66nfWuZ_uWd7Kj9J9QQ-YvpqxSg5AJhhczNTZt6nvmOCPqLA3jnMR-QRqZ_TCARJTte2ghLk9G3SeXIOdLYYumly5NSSjYdMyAuE6dsIi-E59WC2r1cYypp4DG1_kIEb_r2Iw8sZs8DAJPejP2MuQT7rzjvV8nq7qiouu1BIaYSuI35dsovs5WDcGa3oO4nu109HpjuTxX3JFXJkg6tlc1UYnhw8tTg8ruYrIYjDgEff0YlgGFwqjY6DPLEJpyM7i6li1rm7wPdhvkEFryTgiDzOasi0qjXJwLZv3ySWxizNkd8UPmfBuZIrQAAAAHLJqKIbwcl1ia7b5r5R1AjvEpSoJDMLPBqp8zY05YyAFzrs71PgHMz8LcXkJiqYn3iHBFnLNrCzbt3cVBX_1Ko' -H 'Content-Type: application/json' -d '{
  "ExternalId": "mm-154",
  "Name": "Manual mission 14:29:12",
  "MissionType": "Mission",
  "Options": {
    "AllowedMachines": [],
    "Priority": 4,
    "IgnoreAllowedDestinations": false,
    "AllowedAsSecondaryMission": false,
    "SecondaryMissionAllowed": false
  },
  "Steps": [
    {
      "StepType": "Pickup",
      "Options": {
        "Load": {
          "RequiredLoadStatus": "None",
          "RequiredBarcode": "",
          "LoadHeight": 0,
          "StableLoad": true
        },
        "ReservationHandling": "None",
        "MultiReservationRule": "NotAllowed",
        "SortingRules": [
          "Closest"
        ],
        "WaitSortingRules": [
          "ClosestToTarget"
        ],
        "WaitForExtension": false,
        "RequireExternalRelease": false,
        "MinimumExecutionTime": "00:00:00",
        "TargetBufferStackHeight": 0,
        "TargetBufferResourcesInStack": 1,
        "AllowStacking": true,
        "PivotDirection": "ShortestAngle"
      },
      "AllowedTargets": [
        {
          "Id": 1
        }
      ],
      "AllowedWaits": []
    },
    {
      "StepType": "Dropoff",
      "Options": {
        "Load": {
          "RequiredLoadStatus": "None",
          "RequiredBarcode": "",
          "LoadHeight": 0,
          "StableLoad": true
        },
        "ReservationHandling": "None",
        "MultiReservationRule": "NotAllowed",
        "SortingRules": [
          "Closest"
        ],
        "WaitSortingRules": [
          "ClosestToTarget"
        ],
        "WaitForExtension": false,
        "RequireExternalRelease": false,
        "MinimumExecutionTime": "00:00:00",
        "TargetBufferStackHeight": 0,
        "TargetBufferResourcesInStack": 1,
        "AllowStacking": true,
        "PivotDirection": "ShortestAngle"
      },
      "AllowedTargets": [
        {
          "Id": 3
        }
      ],
      "AllowedWaits": []
    },
    {
      "StepType": "Pickup",
      "Options": {
        "Load": {
          "RequiredLoadStatus": "None",
          "RequiredBarcode": "",
          "LoadHeight": 0,
          "StableLoad": true
        },
        "ReservationHandling": "None",
        "MultiReservationRule": "NotAllowed",
        "SortingRules": [
          "Closest"
        ],
        "WaitSortingRules": [
          "ClosestToTarget"
        ],
        "WaitForExtension": false,
        "RequireExternalRelease": false,
        "MinimumExecutionTime": "00:00:00",
        "TargetBufferStackHeight": 0,
        "TargetBufferResourcesInStack": 1,
        "AllowStacking": true,
        "PivotDirection": "ShortestAngle"
      },
      "AllowedTargets": [
        {
          "Id": 5
        }
      ],
      "AllowedWaits": []
    },
    {
      "StepType": "Dropoff",
      "Options": {
        "Load": {
          "RequiredLoadStatus": "None",
          "RequiredBarcode": "",
          "LoadHeight": 0,
          "StableLoad": true
        },
        "ReservationHandling": "None",
        "MultiReservationRule": "NotAllowed",
        "SortingRules": [
          "Closest"
        ],
        "WaitSortingRules": [
          "ClosestToTarget"
        ],
        "WaitForExtension": false,
        "RequireExternalRelease": false,
        "MinimumExecutionTime": "00:00:00",
        "TargetBufferStackHeight": 0,
        "TargetBufferResourcesInStack": 1,
        "AllowStacking": true,
        "PivotDirection": "ShortestAngle"
      },
      "AllowedTargets": [
        {
          "Id": 12
        }
      ],
      "AllowedWaits": []
    }
  ]
}'