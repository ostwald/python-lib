"""
Tasks
"""

def getTasks ():
	import task2, task3, task5, task6, task7, task9, task10, task11, task12, task13

	# itemTasks = map (Task, [task13])
	itemTasks = map (Task, [task2, task3, task5, task6, task7, task9, task10, task11, task12, task13])
	
	if verbose > 1:
		print '\ngetTasks()'
	for task in itemTasks:
		if verbose > 1:
			print '- ', task.name
		task.setVerbose (0)
	
	return itemTasks
