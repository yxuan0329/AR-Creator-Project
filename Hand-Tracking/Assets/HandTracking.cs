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
        // string data2 = udpReceive.data2;

        data = data.Remove(0, 1); // remove left bracket
        data = data.Remove(data.Length - 1, 1);// remove right bracket
        // print(data);
        string[] points = data.Split(',');
        // print(points[0]);

        /*
        data2 = data2.Remove(0, 1); // remove left bracket
        data2 = data2.Remove(data2.Length - 1, 1);// remove right bracket
        // print(data);
        string[] points2 = data2.Split(',');
        // print(points[0]);*/


        // store (x, y, z) to each point
        //0        1*3      2*3
        //x1,y1,z1,x2,y2,z2,x3,y3,z3

        for (int i = 0; i < 21; i++)
        {

            float x = 7 - float.Parse(points[i * 3]) / 80;
            float y = float.Parse(points[i * 3 + 1]) / 90;
            float z = float.Parse(points[i * 3 + 2]) / 100;

            handPoints[i].transform.localPosition = new Vector3(x, y, z);

        }
        /*if (data.Length > 21) // if second hand exists
        {
            for (int i = 21; i < 42; i++)
            {

                float x = 7 - float.Parse(points[i * 3]) / 80;
                float y = float.Parse(points[i * 3 + 1]) / 90;
                float z = float.Parse(points[i * 3 + 2]) / 100;

                handPoints2[i-21].transform.localPosition = new Vector3(x, y, z);

            }
        }*/
        


    }
}