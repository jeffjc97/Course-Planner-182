# Test 1: Least Constrained, No Preference
params['math1a'] = 0
params['math1b'] = 0
params['multi'] = 'MATH25B'
params['linalg'] = 'MATH25A'
params['expos'] = 1
params['max'] = 4
params['preferred_classes'] = []
params['disliked_classes'] = []
params["check_gened"] = False

# Least Constrained, Preference
params['math1a'] = 0
params['math1b'] = 0
params['multi'] = 'MATH23B'
params['linalg'] = 'MATH23A'
params['expos'] = 0
params['max'] = 3
params['preferred_classes'] = ['CS161']
params['disliked_classes'] = ['CS108']
params["check_gened"] = False

# Least Constrained, Gen Eds
params['math1a'] = 0
params['math1b'] = 0
params['multi'] = 'MATH25B'
params['linalg'] = 'MATH25A'
params['expos'] = 1
params['max'] = 4
params['preferred_classes'] = []
params['disliked_classes'] = []
params["check_gened"] = True

# Medium Constrained, Preference, Gen Eds
params['math1a'] = 1
params['math1b'] = 0
params['multi'] = 'MATH23B'
params['linalg'] = 'MATH25A'
params['expos'] = 0
params['max'] = 3
params['preferred_classes'] = ['CS182']
params['disliked_classes'] = []
params["check_gened"] = True

# Most Constrained, Preference, Gen Eds
params['math1a'] = 1
params['math1b'] = 1
params['multi'] = 'MATH21A'
params['linalg'] = 'MATH21B'
params['expos'] = 0
params['max'] = 3
params['preferred_classes'] = ['CS161']
params['disliked_classes'] = ['CS108']
params["check_gened"] = True
