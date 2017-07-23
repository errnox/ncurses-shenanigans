"""
Conventions:
1. The one element in a list which is not a list itself is the hypernym of
   all the other elements in the same list.
2. This hypernym always has to be the first element of a list (though there
   do not have to be other elements in the list).
"""

menustructure = [
    "Menu",
	["Help",
	        ["Some help"]
         ],
	["Colors",
	    	["Red"],
		["Green",
                        ["Light green", ["1"], ["2"], ["3"]],
                        ["Dark green"]
                ],
	        ["Blue",
                         ["Cyan"],
                         ["Cobalt blue"],
                         ["Diamond blue"]
                 ]
         ],
	["Version",
    	        ["Verion 0.1"],
		[""],
                ["Details",
                         ["D 1"],
                         ["D 2"],
                         ["D 3"],
                 ],
		["Test version"]
         ],
         ["Progress bar"]
    ]

