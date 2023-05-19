# The task is to design an algorithm that determines whether or not a given 2SAT instance (a special case of boolean satisfiability problem with 2 literals per clause) has a satisfying assignment. The algorithm does not need to exhibit a satisfying assignment, just decide whether or not one exists.
#
# The algorithm should run in O(m+n) time, where m is the number of clauses and n is the number of variables. The hint suggests that the solution might involve finding strongly connected components in a graph.
#
# To elaborate, in a 2SAT problem, you are given a set of clauses, where each clause is the disjunction (logical OR) of two literals (a literal is a boolean variable or the negation of a boolean variable). The goal is to assign a value "true" or "false" to each of the variables so that all clauses are satisfied, i.e., there is at least one true literal in each clause.