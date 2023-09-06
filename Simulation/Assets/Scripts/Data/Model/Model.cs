using System.Collections.Generic;
using System;
using UnityEngine;

[System.Serializable] // Manejo de clase como una entidad

public class Model {
    public int width;
    public int height;

    public int cells;
    public int garbage;

    public int robots;
    public string positions;

    public int steps;
    public string environment;

    public List<List<string>> mapa;
    public List<Vector3> pos;
}