using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System;

using UnityEngine.Networking;
//using static System.Random;
using UnityEditor;
using UnityEngine; //Para la clase JsonUtility

using System.Net;
using System.IO;

public class APIHelper : MonoBehaviour {
    
    private Model info;
    private float secondsPerRequest;
    private Vector3 fakePos = new Vector3(-1.0f, -1.0f, -1.0f);

    private float x;
    private float z;

    public GameObject robot;
    public List<GameObject> floor = new List<GameObject>(); // Hidden | Discovered
    public List<GameObject> trash = new List<GameObject>(); 
    public List<GameObject> obstacles = new List<GameObject>(); 

    List<GameObject> robotInstances = new List<GameObject>(); 
    List<List<GameObject>> tileInstances = new List<List<GameObject>>(); 
    List<List<GameObject>> trashInstances = new List<List<GameObject>>();
    
    //  IEnumerator:  Fetch the current element from a collection
    // yield return:  Returns a value, but doesn't “close the book” on the function
    IEnumerator SendData(string data, Action doLast) {
        string url = "http://localhost:8585";
        WWWForm form = new WWWForm();

        using (UnityWebRequest request = UnityWebRequest.Post(url, form)) {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data);

            request.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();

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
                foreach(string row in rows) {
                    info.mapa.Add( row.Split(separator, count, StringSplitOptions.RemoveEmptyEntries).ToList() );
                }

                /*string map = "";
                for(int i = 0; i < rows.Length; i++) {
                    foreach(string col in info.mapa[i]) {
                        map += col + "-";
                    }
                    map += "/";
                }
                Debug.Log(map);*/
                
                //yield return JsonUtility.FromJson<Model>(json);
            }
            
            doLast();
        }
    }

    void Start() {
        secondsPerRequest = 0.5f;
        
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

                // Cambiar para instanciar en el lugar correcto y monitorearlos
                int basura;
                bool isNumeric = int.TryParse(info.mapa[i][j], out basura);

                if (isNumeric) {
                    for(int k = 0; k < basura; k++){
                        System.Random rnd = new System.Random();
                        System.Random rnd2 = new System.Random();
                        Instantiate(trash[ rnd.Next(0, trash.Count - 1) ], new Vector3((float)rnd2.NextDouble() * ((x + 1f) - (x - 1f)) + (x - 1f), 1f, (float)rnd2.NextDouble() * ((z + 1f) - (z - 1f)) + (z - 1f)), Quaternion.identity);
                    }
                }
                
                x += 2;
            }
            z -= 2;
            x = 0;
        }
    }
}
