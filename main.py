from flask import Flask, render_template
import json


class CandidateFactory:
    candidates = {}

    def create_candidates_from_json(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            for parsed_item in json.load(file):
                _id = parsed_item['id']
                _name = parsed_item['name']
                _picture = parsed_item['picture']
                _position = parsed_item['position']
                _gender = parsed_item['gender']
                _age = parsed_item['age']
                _skills = parsed_item['skills']

                # Create candidate object and register it in dictionary
                self.candidates[_id] = Candidate(_id, _name, _picture, _position, _gender, _age, _skills)

    def get_by_skill(self, skill_name):

        candidate_list = []
        for candidate in self.candidates.values():
            if candidate.has_skill(skill_name):
                candidate_list.append(candidate)

        if len(candidate_list) == 0:
            return None
        else:
            return candidate_list


class Candidate:

    def __init__(self, id, name, picture, position, gender, age, skills):
        self.id = id
        self.name = name
        self.picture = picture
        self.position = position
        self.gender = gender
        self.age = age
        self.skills = skills
        self.skills_set = set(self.skills.lower().split(', '))

    def has_skill(self, skill_name):
        return skill_name.lower() in self.skills_set


candidateDB = CandidateFactory()
candidateDB.create_candidates_from_json('candidates.json')

app = Flask(__name__)


@app.route("/")
def page_index():
    return render_template("index.html", candidates=candidateDB.candidates)


@app.route("/candidate/<int:uid>")
def page_profile(uid):
    if uid in candidateDB.candidates.keys():
        candidate = candidateDB.candidates[uid]
        return render_template("candidate.html", candidate=candidate)
    else:
        return render_template("not_found.html")


@app.route("/skill/<skill_name>")
def page_skill(skill_name):
    skilled_candidates = candidateDB.get_by_skill(skill_name)

    if skilled_candidates is None:
        return render_template("not_found.html")
    else:
        return render_template("skill.html", candidates=skilled_candidates)


app.run(debug=True)
