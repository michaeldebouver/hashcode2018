from main import hashcode_a_b_c, hashcode_e, hashcode_d


score_a = hashcode_a_b_c.run_first_scenario()
score_b = hashcode_a_b_c.run_second_scenario()
score_c = hashcode_a_b_c.run_third_scenario()
score_d = hashcode_d.run_fourth_scenario()
score_e = hashcode_e.run_fifth_scenario()

full_score = score_a + score_b + score_c +score_d + score_e
print("The full score is: "+str(full_score))
