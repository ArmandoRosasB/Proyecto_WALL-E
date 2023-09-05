using System.Collections.Generic;
using System;

[System.Serializable] // Manejo de clase como una entidad

public class Model {
    public int width;
    public int height;

    public int cells;
    public int garbage;

    public int robots;
    public List<List<float>> pos;

    public int steps;
    public string environment;

    public List<List<string>> mapa;
}