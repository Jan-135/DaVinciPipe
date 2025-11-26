import gazu

basePath = "N:/"
productionName = "hamster"


def start():
    allProjects = gazu.client.get("/data/projects/all")
    kitsuProject = [project for project in allProjects if project["name"] == productionName][0]
    kitsuProjectId = kitsuProject.get("id")
    kitsuFilter = {"project_id": kitsuProjectId}
    allShots = gazu.client.get("/data/shots", params=kitsuFilter)
    setAbsolutepathForEveryShot(allShots)

def setAbsolutepathForEveryShot(shotlist: list[dict]):
    for shot in shotlist:
        print(shot)

        path = getPreviewPath(shot)
        shot["data"]["absolutepath"] = path
        print(path)
        gazu.shot.update_shot(shot)

def getPreviewPath(shot: dict):
    path = basePath + productionName + "/Shots/" + shot["sequence_name"] + "/" + shot["name"] + "/Layout/standalone/publish/previews"
    return path