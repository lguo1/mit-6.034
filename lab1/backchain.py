from production import AND, OR, NOT, PASS, FAIL, IF, THEN, \
     match, populate, simplify, variables
from zookeeper import ZOOKEEPER_RULES

# This function, which you need to write, takes in a hypothesis
# that can be determined using a set of rules, and outputs a goal
# tree of which statements it would need to test to prove that
# hypothesis. Refer to the problem set (section 2) for more
# detailed specifications and examples.

# Note that this function is supposed to be a general
# backchainer.  You should not hard-code anything that is
# specific to a particular rule set.  The backchainer will be
# tested on things other than ZOOKEEPER_RULES.


def backchain_to_goal_tree(rules, hypothesis):
    OR_list = [hypothesis]
    for rule in rules:
        for con in rule.consequent():
            bindings = match(con, hypothesis)
            if bindings is not None:
                ant = rule.antecedent()
                if isinstance(ant, str):
                    new_hypo = populate(ant, bindings)
                    OR_list.append(backchain_to_goal_tree(rules, new_hypo))
                elif isinstance(ant, AND):
                    lst = []
                    for term in ant:
                        new_hypo = populate(term, bindings)
                        lst.append(backchain_to_goal_tree(rules, new_hypo))
                    OR_list.append(AND(lst))
                else:
                    lst = []
                    for term in ant:
                        new_hypo = populate(term, bindings)
                        lst.append(backchain_to_goal_tree(rules, new_hypo))
                    OR_list.append(OR(lst))
                break
    return simplify(OR(OR_list))


# Here's an example of running the backward chainer - uncomment
# it to see it work:
print backchain_to_goal_tree(ZOOKEEPER_RULES, 'opus is a penguin')
