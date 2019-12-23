varying vec3 camera_pos;

void main() {
    camera_pos = normalize(vec3(gl_ModelViewMatrix * gl_Vertex));
    gl_Position = ftransform();
}
