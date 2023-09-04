// TC2008B Modelación de Sistemas Multiagentes con gráficas computacionales
// C# client to interact with Python server via POST
// Sergio Ruiz-Loza, Ph.D. March 2021

using System.Collections.Generic;
using System.Collections;

using UnityEngine.Networking;
using UnityEditor;
using UnityEngine;

public class WebClientTest : MonoBehaviour {
    private float secondsPerRequest;
    
    //  IEnumerator:  Fetch the current element from a collection
    // yield return:  Returns a value, but doesn't “close the book” on the function
    IEnumerator SendData(string data) {
        string url = "http://localhost:8585";
        
        WWWForm form = new WWWForm();
        //form.AddField("bundle", "the data"); // ???

        using (UnityWebRequest request = UnityWebRequest.Post(url, form)) {
            byte[] bodyRaw = System.Text.Encoding.UTF8.GetBytes(data); // data??

            request.uploadHandler = (UploadHandler)new UploadHandlerRaw(bodyRaw);
            request.downloadHandler = (DownloadHandler)new DownloadHandlerBuffer();

            request.SetRequestHeader("Content-Type", "application/json"); // "text/html"

            yield return request.SendWebRequest(); // Talk to Python

            if(request.isNetworkError || request.isHttpError) { 
                Debug.Log(request.error);
            
            } else {
                Debug.Log(request.downloadHandler.text); // Answer from Python
                char[,] info = JsonUtility.FromJson<Vector3>(request.downloadHandler.text.Replace('\'', '\"'));
                
                //Debug.Log("Form upload complete!");
                Debug.Log(tPos);
            }
        }
    }

    void Start() {
        secondsPerRequest = 1;

    }

    void Update() {
        if(secondsPerRequest <= 0) {
            Vector3 fakePos = new Vector3(-1.0f, -1.0f, -1.0f);

            string json = EditorJsonUtility.ToJson(fakePos);
            StartCoroutine(SendData(json));

            secondsPerRequest = 1;
        } else {
            secondsPerRequest -= Time.deltaTime;
        }
    }
}
