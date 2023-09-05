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
    
    private Model info;
    private bool explorar;
    private float secondsPerRequest;
    private Vector3 fakePos = new Vector3(-1.0f, -1.0f, -1.0f);

    private float x;
    private float z;
    private System.Random rndInt = new System.Random();
    private System.Random rndFlt = new System.Random();

    public GameObject robot;
    public GameObject papelera;
    public List<GameObject> floor = new List<GameObject>(); // Hidden | Discovered
    public List<GameObject> trash = new List<GameObject>(); 
    public List<GameObject> obstacle = new List<GameObject>(); 
    
    public List<Tuple<int, int>> obstacles = new List<Tuple<int, int>>(); 

    private List<GameObject> robotInstances = new List<GameObject>(); 
    private List<List<GameObject>> tileInstances = new List<List<GameObject>>(); 
    private List<List<GameObject>> trashInstances = new List<List<GameObject>>();
    
    //  IEnumerator:  Fetch the current element from a collection
    // yield return:  Returns a value, but doesn't “close the book” on the function
    IEnumerator SendData(string data, Action doLast) {
        string url = "http://localhost:8585";
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

                String[] separator = {","};
                int count = info.width;
                String[] rows = info.environment.Split(separator, count, StringSplitOptions.RemoveEmptyEntries);
            
                info.mapa = new List<List<string>>();
                separator[0] = "*";
                count = info.height;

                for(int i = 0; i < info.width; i++) {
                    info.mapa.Add(rows[i].Split(separator, count, StringSplitOptions.RemoveEmptyEntries).ToList());
                }

                // ----------------------------------------------------------
                /*string map = "";
                for(int i = 0; i < info.mapa.Count; i++) {

                    for(int j = 0; j < info.mapa[i].Count; j++) {
                        map += info.mapa[i][j];

                        if(j != info.mapa[i].Count - 1){
                            map += "/";
                        }
                    }

                    if(i != info.mapa.Count - 1){
                        map += "/";
                    }
                }
                Debug.Log(map);*/
                // ----------------------------------------------------------
            }

            doLast();
        }
    }

    void Start() {
        secondsPerRequest = 0.5f;
        explorar = true;
        
        string json = EditorJsonUtility.ToJson(fakePos);
        StartCoroutine( SendData(json,DoLastStart) );
    }

    void DoLastStart() {
        x = 0;
        z = 0;

        for(int i = 0; i < info.width; i++){
            tileInstances.Add(new List<GameObject>());

            for(int j = 0; j < info.height; j++){
                GameObject tile = Instantiate(floor[0], new Vector3(x, 0f, z), Quaternion.identity);
                tileInstances[i].Add(tile);

                /*if(i == 4 && j == 6) {
                    Debug.Log(info.mapa[i][j]);
                }*/

                if(info.mapa[i][j].Trim() == "X") {
                    Instantiate(obstacle[ rndInt.Next(0, obstacle.Count - 1) ], new Vector3(x, 1f, z), Quaternion.identity);

                } else if(info.mapa[i][j].Trim() == "P") {
                    Instantiate(papelera, new Vector3(x, 1f, z), Quaternion.identity);

                } if(info.mapa[i][j].Trim() == "S") {
                    info.pos = new List<List<float>>();

                    for(int r = 0; r < info.robots; r++) {
                        GameObject newRobot = Instantiate(robot, new Vector3(x, 1f, z), Quaternion.identity);
                        
                        info.pos.Add(new List<float>());
                        info.pos[r].Add(x);
                        info.pos[r].Add(z);

                        robotInstances.Add(newRobot);
                    }
                }
                // FALTA else{ Instanciar basura }

                x += 2;
            }
            z -= 2;
            x = 0;
        }

        // Add robot
        //GameObject robot = Instantiate(----, new Vector3(x, 0f, z), Quaternion.identity);
    }

    void Update() {
        if(secondsPerRequest <= 0) {
            string json = EditorJsonUtility.ToJson(fakePos);
            StartCoroutine( SendData(json,DoLastUpdate) );

            secondsPerRequest = 0.5f;
        } else {
            secondsPerRequest -= Time.deltaTime;
        }
    }

    void DoLastUpdate() {
        x = 0;
        z = 0;

        if(explorar == true) {
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

            if(info.cells == 0) {
                explorar = false;
            }
        }

        /*for(int i = 0; i < info.width; i++){
            for(int j = 0; j < info.height; j++){
                GameObject tile = tileInstances[i][j];
                Destroy(tile);

                if (info.mapa[i][j] == "-1"){
                    tile = Instantiate(floor[0], new Vector3(x, 0f, z), Quaternion.identity);
                } else {
                    tile = Instantiate(floor[1], new Vector3(x, 0f, z), Quaternion.identity);
                }
                tileInstances[i][j] = tile;

                // Obstáculos
                if (info.mapa[i][j] == "X" && !obstacles.Contains(Tuple.Create(i,j))){
                    Instantiate(obstacle[ rndInt.Next(0, obstacle.Count - 1) ], new Vector3(x, 0f, z), Quaternion.identity);
                    obstacles.Add(Tuple.Create(i,j));
                }*/

                // Cambiar para instanciar en el lugar correcto y monitorearlos
                /*int basura;
                bool isNumeric = int.TryParse(info.mapa[i][j], out basura);

                if (isNumeric) {
                    for(int k = 0; k < basura; k++){
                        System.Random rnd = new System.Random();
                        System.Random rnd2 = new System.Random();
                        Instantiate(trash[ rnd.Next(0, trash.Count - 1) ], new Vector3((float)rnd2.NextDouble() * ((x + 1f) - (x - 1f)) + (x - 1f), 1f, (float)rnd2.NextDouble() * ((z + 1f) - (z - 1f)) + (z - 1f)), Quaternion.identity);
                    }
                }*//*
                
                x += 2;
            }
            z -= 2;
            x = 0;
        }*/
    }
}
