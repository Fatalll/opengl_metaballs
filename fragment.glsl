#extension GL_OES_standard_derivatives : enable

varying vec3 camera_pos;

void main() {
    vec3 normal  = normalize(cross(dFdx(camera_pos), dFdy(camera_pos)));

    vec4 light_dir = gl_ModelViewProjectionMatrix * vec4(1.0, -1.0, -1.0, 0.0);
    vec3 light_vec = normalize(light_dir.xyz);

    float diffuse = 0.6 * max(dot(normal, light_vec), 0.0);

    gl_FragColor = vec4(diffuse * vec3(0.2, 0.3, 0.9), 1.0);
}