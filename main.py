from flask import Flask, render_template
import json

app = Flask(__name__)




class CandidateFactory():
    candidates = {}

    def get_candidates_from_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            _temp = json.load(file)

            for candi in _temp:
                cand = Candidate(candi['id'], candi['name'], candi['picture'], candi['position'], candi['gender'], candi['age'], candi['skills'])
                self.candidates[candi['id']] = cand


    def get_by_skill(self, skill_name):

        candidate_slice = []
        for id, candidate in self.candidates.items():
            if candidate.has_skill(skill_name):
                candidate_slice.append(candidate)

        if len(candidate_slice) == 0:
            return None
        else:
            return candidate_slice






class Candidate():

    def __init__(self, id, name, picture, position, gender, age, skills):
        self.id = id
        self.name = name
        self.picture = picture
        self.position = position
        self.gender = gender
        self.age = age
        self.skills = skills.split(', ')



    def has_skill(self, skill_name):
        return skill_name in self.skills



factory = CandidateFactory()

factory.get_candidates_from_json('candidates.json')

print(factory.candidates)

print(factory.get_by_skill('python'))



@app.route("/")
def page_index():
    return render_template("index.html", candidates=factory.candidates)

@app.route("/candidate/<int:uid>")
def page_profile(uid):
    return render_template("candidate.html", candidate=factory.candidates[uid])

@app.route("/skill/<skill_name>")
def page_skill(skill_name):

    skilled_candidates = factory.get_by_skill(skill_name)

    if skilled_candidates is None:
        return render_template("not_found.html")
    else:
        return render_template("skill.html", candidates=skilled_candidates)

app.run(debug=True)
