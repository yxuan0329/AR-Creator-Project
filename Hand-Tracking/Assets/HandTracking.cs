using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class HandTracking : MonoBehaviour
{
    // Start is called before the first frame update
    public UDPReceive udpReceive;
    public GameObject[] handPoints, handPoints2;
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        string data = udpReceive.data;

        data = data.Remove(0, 1); // remove left bracket
        data = data.Remove(data.Length - 1, 1);// remove right bracket
        string[] points = data.Split(',');


        // store (x, y, z) to each point
        //0        1*3      2*3
        //x1,y1,z1,x2,y2,z2,x3,y3,z3

        if (data.Length > 0)
        {
            for (int i = 0; i < 21; i++)
            {

                float x = 9 - float.Parse(points[i * 3]) / 30;
                float y = float.Parse(points[i * 3 + 1]) / 50;
                float z = float.Parse(points[i * 3 + 2]) / 50;

                Debug.Log("x=" + x + ", y=" + y + ", z=" + z);
                handPoints[i].transform.localPosition = new Vector3(x, y, z);

            }
        }
        if (data.Length > 63) // if second hand exists
        {
            for (int i = 21; i < 42; i++)
            {

                float x = 9 - float.Parse(points[i * 3]) / 30;
                float y = float.Parse(points[i * 3 + 1]) / 50;
                float z = float.Parse(points[i * 3 + 2]) / 50;

                handPoints2[i-21].transform.localPosition = new Vector3(x, y, z);

            }
        }
        


    }
}