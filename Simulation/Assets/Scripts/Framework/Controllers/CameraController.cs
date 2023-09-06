using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour {
    public static float x;
    public static float z;
    public static bool flag;
    private bool modifyOffset;

    private Vector3 offset = new Vector3(0,5,0);

    private Model reference;
    private List<GameObject> robots;

    // Start is called before the first frame update
    void Start() {
        flag = false;
        modifyOffset = false;

    }

    // Update is called once per frame
    void LateUpdate() {
        if (flag) {
            reference = APIHelper.info;
            robots = APIHelper.robotInstances;
            
            if (!modifyOffset){
                x = x / 2;
                z = (z / 2) + 1;
                modifyOffset = true;
            }
            transform.position = new Vector3(x, 27.2f, z);







        }
       
    }
}
