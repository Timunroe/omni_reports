config = {
    "report": {
        "daily": {
            "record": {
                "pdf_name": "pdfs_new/DailyRec.pdf",
                "site": "Record",
                "report": "daily",
                "fetch_limits": {
                    "Twitter": 3,
                    "Facebook": 3,
                    "top stories": 3
                },
                "sections": [
                    {
                        "name": "report date",
                        "trim": [None, None],
                        "remove": [],
                        "subs": [
                            ["Mar.", "March"],
                            ["Mon.", "Monday"],
                            ["Tue.", "Tuesday"],
                            ["Wed.", "Wednesday"],
                            ["Thu.", "Thursday"],
                            ["Fri.", "Friday"],
                            ["Sat.", "Saturday"],
                            ["Sun.", "Sunday"],
                        ],
                        "keys": [
                            ("day", 0),
                            ("date", 1),
                            ("month", 2),
                            ("year", 3),
                        ],
                        "markers": {
                            "start": "Company Summary",
                            "end": "Report Suite"
                        }
                    },
                    {
                        "name": "summary ys",
                        "trim": [2, -1],
                        "remove": [","],
                        "subs": [
                            ["AR Dailies and Communities (formally DNN Local)", "Metroland"],
                            ["vrs_torsta3_arthespec", "Spectator"],
                            ["vrs_torsta3_artherecord", "Record"],
                            ["vrs_torsta3_arguelphmercurytribu", "MercTrib"],
                            ["vrs_torsta3_arcambridgetimes", "CTimes"],
                            ["vrs_torsta3_arwaterloochronicle", "WChronicle"],
                            ["vrs_torsta3_arkitchenerpost", "KPost"],
                            ["vrs_torsta3_arnewhamburgindepend", "NHIndepend"]
                        ],
                        "keys": [
                            ("name", 0),
                            ("pv", 1),
                            ("uv", 2),
                            ("v", 3),
                        ],
                        "markers": {
                            "start": "Company Summary",
                            "end": "Company Summary L90"
                        }
                    },
                    {
                        "name": "summary l90",
                        "trim": [2, -4],
                        "remove": [","],
                        "subs": [
                            ["AR Dailies and Communities (formally DNN Local)", "Metroland"],
                            ["vrs_torsta3_arthespec", "Spectator"],
                            ["vrs_torsta3_artherecord", "Record"],
                            ["vrs_torsta3_arguelphmercurytribu", "MercTrib"],
                            ["vrs_torsta3_arcambridgetimes", "CTimes"],
                            ["vrs_torsta3_arwaterloochronicle", "WChronicle"],
                            ["vrs_torsta3_arkitchenerpost", "KPost"],
                            ["vrs_torsta3_arnewhamburgindepend", "NHIndepend"]
                        ],
                        "keys": [
                            ("name", 0),
                            ("pv_l90", 1),
                            ("uv_l90", 2),
                            ("v_l90", 3),
                        ],
                        "markers": {
                            "start": "Company Summary L90",
                            "end": "Summary yesterday"
                        }
                    },
                    {
                        "name": "referring domains ys",
                        "trim": [3, -4],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                            ("domain", 1),
                            ("pv", 2)
                        ],
                        "markers": {
                            "start": "Ref Domains yesterday",
                            "end": "Ref Domains L90"
                        }
                    },
                    {
                        "name": "referring domains l90",
                        "trim": [3, -4],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                            ("domain", 1),
                            ("pv_l90", 2)
                        ],
                        "markers": {
                            "start": "Ref Domains L90",
                            "end": "Device Type yesterday"
                        }
                    },
                    {
                        "name": "top stories",
                        "trim": [3, -4],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                            ("asset", 1),
                            ("pv", 2),
                            ("%", 3)
                        ],
                        "markers": {
                            "start": "Top AssetIDs yesterday",
                            "end": "FB top stories ys"
                        }
                    },
                    {
                        "name": "facebook top stories",
                        "trim": [4, None],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                            ("asset", 1),
                            ("pv", 2)
                        ],
                        "markers": {
                            "start": "FB top stories ys",
                            "end": "Tco top stories ys"
                        }
                    },
                    {
                        "name": "twitter top stories",
                        "trim": [4, -1],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                            ("asset", 1),
                            ("pv", 2)
                        ],
                        "markers": {
                            "start": "Tco top stories ys",
                            "end": "Page 7 of 7"
                        }
                    },
                    {
                        "name": "device types ys",
                        "trim": [3, -1],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                            ("name", 1),
                            ("pv", 2),
                            ("%", 3)
                        ],
                        "markers": {
                            "start": "Device Type yesterday",
                            "end": "Device Type l90"
                        }
                    },
                    {
                        "name": "device types l90",
                        "trim": [3, -4],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                            ("name", 1),
                            ("pv_l90", 2),
                            ("%_l90", 3)
                        ],
                        "markers": {
                            "start": "Device Type l90",
                            "end": "Top AssetIDs yesterday"
                        }
                    }
                ]
            },
            "spectator": {
                "pdf_name": "pdfs_new/DailySpec.pdf",
                "site": "Spectator",
                "report": "daily",
                "fetch_limits": {
                    "Twitter": 3,
                    "Facebook": 3,
                    "top stories": 5
                },
                "sections": [
                    {
                        "name": "report date",
                        "trim": [None, None],
                        "remove": [],
                        "subs": [
                            ["Mar.", "March"],
                            ["Mon.", "Monday"],
                            ["Tue.", "Tuesday"],
                            ["Wed.", "Wednesday"],
                            ["Thu.", "Thursday"],
                            ["Fri.", "Friday"],
                            ["Sat.", "Saturday"],
                            ["Sun.", "Sunday"],
                        ],
                        "keys": [
                            ("day", 0),
                            ("date", 1),
                            ("month", 2),
                            ("year", 3),
                        ],
                        "markers": {
                            "start": "Sites summary yesterday",
                            "end": "Report Suite"
                        }
                    },
                    {
                        "name": "summary ys",
                        "trim": [2, -4],
                        "remove": [","],
                        "subs": [
                            ["AR Dailies and Communities (formally DNN Local)", "Metroland"],
                            ["vrs_torsta3_arthespec", "Spectator"],
                            ["vrs_torsta3_artherecord", "Record"],
                            ["vrs_torsta3_arguelphmercurytribu", "MercTrib"],
                            ["vrs_torsta3_ardurhamregion", "Durham"],
                            ["vrs_torsta3_arinsidehalton", "Halton"],
                            ["vrs_torsta3_arstcatharinesstanda", "Standard"],
                            ["vrs_torsta3_arpeterboroughexamin", "Examiner"],
                            ["vrs_torsta3_arniagarafallsreview", "NFReview"],
                            ["vrs_torsta3_arwellandtribune", "WTribune"],
                            ["vrs_torsta3_aryorkregion", "YorkReg"]
                        ],
                        "keys": [
                            ("name", 0),
                            ("pv", 1),
                            ("uv", 2),
                            ("v", 3),
                        ],
                        "markers": {
                            "start": "Sites summary yesterday",
                            "end": "Sites summary L90"
                        }
                    },
                    {
                        "name": "summary l90",
                        "trim": [2, -4],
                        "remove": [","],
                        "subs": [
                            ["AR Dailies and Communities (formally DNN Local)", "Metroland"],
                            ["vrs_torsta3_arthespec", "Spectator"],
                            ["vrs_torsta3_artherecord", "Record"],
                            ["vrs_torsta3_arguelphmercurytribu", "MercTrib"],
                            ["vrs_torsta3_ardurhamregion", "Durham"],
                            ["vrs_torsta3_arinsidehalton", "Halton"],
                            ["vrs_torsta3_arstcatharinesstanda", "Standard"],
                            ["vrs_torsta3_arpeterboroughexamin", "Examiner"],
                            ["vrs_torsta3_arniagarafallsreview", "NFReview"],
                            ["vrs_torsta3_arwellandtribune", "WTribune"],
                            ["vrs_torsta3_aryorkregion", "YorkReg"]
                        ],
                        "keys": [
                            ("name", 0),
                            ("pv_l90", 1),
                            ("uv_l90", 2),
                            ("v_l90", 3),
                        ],
                        "markers": {
                            "start": "Sites summary L90",
                            "end": "Ref Domains yesterday"
                        }
                    },
                    {
                        "name": "referring domains ys",
                        "trim": [3, -4],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                                ("domain", 1),
                                ("pv", 2)
                        ],
                        "markers": {
                            "start": "Ref Domains yesterday",
                            "end": "Ref Domains L90"
                        }
                    },
                    {
                        "name": "referring domains l90",
                        "trim": [3, -4],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                                ("domain", 1),
                                ("pv_l90", 2)
                        ],
                        "markers": {
                            "start": "Ref Domains L90",
                            "end": "Top Asset ID yesterday"
                        }
                    },
                    {
                        "name": "top stories",
                        "trim": [3, -1],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                                ("asset", 1),
                                ("pv", 2),
                                ("%", 3)
                        ],
                        "markers": {
                            "start": "Top Asset ID yesterday",
                            "end": "Durham Top Asset ID ys"
                        }
                    },
                    {
                        "name": "facebook top stories",
                        "trim": [4, None],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                                ("asset", 1),
                                ("pv", 2)
                        ],
                        "markers": {
                            "start": "FB top stories ys",
                            "end": "Tco top stories ys"
                        }
                    },
                    {
                        "name": "twitter top stories",
                        "trim": [4, -3],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                                ("asset", 1),
                                ("pv", 2)
                        ],
                        "markers": {
                            "start": "Tco top stories ys",
                            "end": "Device Type yesterday"
                        }
                    },
                    {
                        "name": "device types ys",
                        "trim": [3, -1],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                                ("name", 1),
                                ("pv", 2),
                                ("%", 3)
                        ],
                        "markers": {
                            "start": "Device Type yesterday",
                            "end": "Device Type L90"
                        }
                    },
                    {
                        "name": "device types l90",
                        "trim": [3, -1],
                        "remove": [",", "%"],
                        "targets": [],
                        "subs": [],
                        "keys": [
                                ("name", 1),
                                ("pv_l90", 2),
                                ("%_l90", 3)
                        ],
                        "markers": {
                            "start": "Device Type L90",
                            "end": "Page 8 of 8"
                        }
                    }
                ]
            }
        }
    }
}





       # "weekly": {
       #      "Spec": {
       #          "pdf_name": "pdfs_new/weekly.pdf",
       #          "site": "Spec",
       #      "sections": [
       #          {
       #              "name": "summary last week",
       #              "filter_lines": "number-comma",
       #              "trim": [3, -3],
       #              "remove": [',', '%', 'Spent', 'Weekly'],
       #              "subs": [
       #                  ['Average', 'Avg'],
       #                  ['Signup Clicks', 'Signups'],
       #                  [' Media / Email', '-email'],
       #              ],
       #              "keys": [
       #                  # tuples where [0] is field name, [1] is field position
       #                  ('metric', 0),
       #                  ('value', 1),
       #              ],
       #              "markers": {
       #                  "start": "Summary last week",
       #                  "end": "Summary 3 mos"
       #              }
       #          },
       #          {
       #              "name": "summary L90",
       #              "filter_lines": "number-comma",
       #              "trim": [3, -3],
       #              "remove": [',', '%', 'Spent', 'Weekly'],
       #              "subs": [
       #                  ['Average', 'Avg'],
       #                  ['Signup Clicks', 'Signups'],
       #                  [' Media / Email', '-email'],
       #              ],
       #              "keys": [
       #                  ('metric', 0),
       #                  ('value', 1),
       #              ],
       #              "markers": {
       #                  "start": "Summary 3 mos",
       #                  "end": "PageViews compare"
       #              }
       #          },
       #          # {
       #          #     "name": "Referring domains yesterday",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('domain', 1),
       #          #         ('pv', 2)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "Ref Domains yesterday",
       #          #         "end": "Ref Domains L90"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "Referring domains L90",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('domain', 1),
       #          #         ('pv_l90', 2)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "Ref Domains L90",
       #          #         "end": "Top Asset ID yesterday"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "Spec top stories",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('asset', 1),
       #          #         ('pv', 2),
       #          #         ('%', 3)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "Top Asset ID yesterday",
       #          #         "end": "Durham Top Asset ID ys"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "Durham top stories",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('asset', 1),
       #          #         ('pv', 2),
       #          #         ('%', 3)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "Durham Top Asset ID ys",
       #          #         "end": "York Top Asset ID ys"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "York top stories",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('asset', 1),
       #          #         ('pv', 2),
       #          #         ('%', 3)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "York Top Asset ID ys",
       #          #         "end": "Halton Top Asset ID ys"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "Halton top stories",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('asset', 1),
       #          #         ('pv', 2),
       #          #         ('%', 3)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "Halton Top Asset ID ys",
       #          #         "end": "FB top stories ys"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "Facebook top stories",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('rank', 0),
       #          #         ('asset', 1),
       #          #         ('pv', 2),
       #          #         ('%', 3)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "FB top stories ys",
       #          #         "end": "Tco top stories ys"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "Twitter top stories",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('rank', 0),
       #          #         ('asset', 1),
       #          #         ('pv', 2),
       #          #         ('%', 3)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "Tco top stories ys",
       #          #         "end": "Device Type yesterday"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "Device types yesterday",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('rank', 0),
       #          #         ('name', 1),
       #          #         ('pv', 2),
       #          #         ('%', 3)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "Device Type yesterday",
       #          #         "end": "Device Type L90"
       #          #     },
       #          # },
       #          # {
       #          #     "name": "Device types L90",
       #          #     "filter_lines": "percent",
       #          #     "remove": [',', '%'],
       #          #     "targets": [],
       #          #     "subs": [],
       #          #     "keys": [
       #          #         ('name', 1),
       #          #         ('pv_l90', 2),
       #          #         ('%_l90', 3)
       #          #     ],
       #          #     "markers": {
       #          #         "start": "Device Type L90",
       #          #         "end": "Page 8 of 8"
       #          #     },
       #          # }
       #      ]
       #  },
