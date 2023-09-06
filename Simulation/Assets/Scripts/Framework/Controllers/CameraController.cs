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

    [SerializeField]
    private float horizontal;

    [SerializeField]
    private float vertical;


    private float speed = 5f;

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
                transform.position = new Vector3(x, 27.2f, z);
                modifyOffset = true;
            }
           
        }

        horizontal = Input.GetAxis("Horizontal");
        vertical = Input.GetAxis("Vertical");

        transform.Translate(Vector3.forward * Time.deltaTime * speed * vertical);
        transform.Translate(Vector3.right * Time.deltaTime * speed * horizontal);
       
    }
}
