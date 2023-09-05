using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraController : MonoBehaviour {
    private float x;
    private float y;
    private float z;
    public static bool flag;

    private Model reference;

    // Start is called before the first frame update
    void Start() {
        flag = false;
    }

    // Update is called once per frame
    void LateUpdate() {
        if (flag) {
            reference = APIHelper.info;

            y = 27.3f;
            x = reference.width / 2;
            z = reference.height / 2;

            transform.position = new Vector3(x, y, z);
        }
       
    }
}
