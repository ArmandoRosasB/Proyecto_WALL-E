using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System;

using UnityEngine.Networking;
using UnityEditor;
using UnityEngine; //Para la clase JsonUtility

using System.Net;
using System.IO;

public class APIHelper : MonoBehaviour {
    
    public static Model info;

    private float timer;
    private float secondsPerRequest;
    private Vector3 fakePos = new Vector3(-1.0f, -1.0f, -1.0f);

    private float x;
    public float y;
    private float z;
    private System.Random rndInt = new System.Random();
    private System.Random rndFlt = new System.Random();

    public Light dirLight;
    private bool change;

    public GameObject robot;
    public GameObject papelera;
    public List<GameObject> floor = new List<GameObject>(); // Hidden | Discovered
    public List<GameObject> trash = new List<GameObject>(); 
    public List<GameObject> obstacle = new List<GameObject>(); 

    public static List<GameObject> robotInstances = new List<GameObject>(); 
    private List<List<GameObject>> tileInstances = new List<List<GameObject>>(); 
    private List<List<List<GameObject>>> trashInstances = new List<List<List<GameObject>>>();
    
    //  IEnumerator:  Fetch the current element from a collection
    // yield return:  Returns a value, but doesn't “close the book” on the function
    IEnumerator SendData(string data, Action doLast) {
        string url = "http://10.25.93.243:8585";
        WWWForm form = new WWWForm();

        using (UnityWebRequest request = UnityWebRequest.Post(url, form)) {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);

            request.uploadHandler = (UploadHandler) new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = (DownloadHandler) new DownloadHandlerBuffer();

            request.SetRequestHeader("Content-Type", "application/json"); // "text/html"

            yield return request.SendWebRequest(); // Talk to Python

            if(request.isNetworkError || request.isHttpError) { 
                Debug.Log(request.error);
            
            } else {
                string json = request.downloadHandler.text.Replace('\'', '\"'); // Answer from Python
                info = JsonUtility.FromJson<Model>(json);

                // Reconstruimos el mapa
                info.mapa = new List<List<string>>();
                String[] rows = info.environment.Split(",", info.width, StringSplitOptions.RemoveEmptyEntries);
                
                for(int i = 0; i < info.width; i++) {
                    info.mapa.Add(rows[i].Split("*", info.height, StringSplitOptions.RemoveEmptyEntries).ToList());
                }

                // Reconstruimos las posiciones
                info.pos = new List<Vector3>();

                rows = info.positions.Split(",", info.robots, StringSplitOptions.RemoveEmptyEntries);

                for(int i = 0; i < info.robots; i++){
                    String [] aux = rows[i].Split("*", 2, StringSplitOptions.RemoveEmptyEntries);
                    info.pos.Add(new Vector3((float)Convert.ToDouble(aux[0]), 1f, (float)Convert.ToDouble(aux[1])));
                }
            }

            doLast();
        }
    }

    void Start() {
        dirLight.enabled = false;

        secondsPerRequest = 0.25f;
        timer = secondsPerRequest;
        
        string json = EditorJsonUtility.ToJson(fakePos);
        StartCoroutine( SendData(json,DoLastStart) );
    }

    void DoLastStart() {
        x = 0;
        z = 0;

        CameraController.flag = true;

        for(int i = 0; i < info.width; i++){
            tileInstances.Add(new List<GameObject>());
            trashInstances.Add(new List<List<GameObject>>());

            for(int j = 0; j < info.height; j++){
                GameObject tile = Instantiate(floor[0], new Vector3(x, 0f, z), Quaternion.identity);
                
                tileInstances[i].Add(tile);
                trashInstances[i].Add(new List<GameObject>());

                if(info.mapa[i][j].Trim() == "X") {
                    Instantiate(obstacle[ rndInt.Next(0, obstacle.Count - 1) ], new Vector3(x, 1.5f, z), Quaternion.identity);

                } else if(info.mapa[i][j].Trim() == "P") {
                    Instantiate(papelera, new Vector3(x, 1f, z), Quaternion.identity);

                } else if(info.mapa[i][j].Trim() == "S") {
                    info.pos = new List<Vector3>();

                    for(int r = 0; r < info.robots; r++) {
                        info.pos.Add(new Vector3(x, 1f, z));
                        GameObject newRobot = Instantiate(robot, info.pos[r], Quaternion.identity);
                        robotInstances.Add(newRobot);
                    }
                
                } else { // Basura
                    int basura;
                    bool isNumeric = int.TryParse(info.mapa[i][j], out basura);

                    if (isNumeric) {
                        for(int k = 0; k < basura; k++){
                            float rango = 0.75f;
                            GameObject newTrash = Instantiate(trash[ rndInt.Next(0, trash.Count - 1) ], new Vector3((float)rndFlt.NextDouble() * ((x + rango) - (x - rango)) + (x - rango), y, (float)rndFlt.NextDouble() * ((z + rango) - (z - rango)) + (z - rango)), Quaternion.identity);
                            trashInstances[i][j].Add(newTrash);
                        }
                    }
                }

                x += 2;
            }
            z -= 2;
            CameraController.x = x;
            x = 0;
        }
        CameraController.z = z;
    }

    void Update() {
        if(timer <= 0) {
            string json = EditorJsonUtility.ToJson(fakePos);
            StartCoroutine( SendData(json,DoLastUpdate) );

            timer = secondsPerRequest; //0.5f;
        } else {
            timer -= Time.deltaTime;
        }
    }

    void DoLastUpdate() {
        x = 0;
        z = 0;

        for(int i = 0; i < info.robots; i++) {
            GameObject bobot = robotInstances[i];
            Destroy(bobot);

            Vector3 auxPos = tileInstances[(int)info.pos[i].x][(int)info.pos[i].z].transform.position;
            GameObject movingRobot = Instantiate(robot, auxPos, Quaternion.identity);
            robotInstances[i] = movingRobot;
        }

        for(int i = 0; i < info.width; i++){
            for(int j = 0; j < info.height; j++){
                GameObject tile = tileInstances[i][j];
                Destroy(tile);

                if (info.mapa[i][j] == "-1"){
                    tile = Instantiate(floor[0], new Vector3(x, 0f, z), Quaternion.identity);
                } else {
                    tile = Instantiate(floor[1], new Vector3(x, 0f, z), Quaternion.identity);
                }
                tileInstances[i][j] = tile;
                
                x += 2;
            }
            z -= 2;
            x = 0;
        }

        for(int i = 0; i < info.width; i++){
            for(int j = 0; j < info.height; j++){
                int basura;
                bool isNumeric = int.TryParse(info.mapa[i][j], out basura);

                if (isNumeric && basura != -1) {
                    if(trashInstances[i][j].Count > basura) {
                        int delete = trashInstances[i][j].Count - basura;

                        for(int d = trashInstances[i][j].Count - 1; d >= 0; d--) {
                            GameObject del = trashInstances[i][j][d];
                            trashInstances[i][j].RemoveAt(d);
                            Destroy(del);
                        }
                    }
                }
            }
        }

        if(info.cells == 0) {
            dirLight.enabled = true;
        }
    }
}
