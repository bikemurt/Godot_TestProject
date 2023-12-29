shader_type spatial;

varying vec3 local_coords;
void vertex() {
	local_coords = VERTEX;
}

void fragment() {
	float y = local_coords.y / 0.491 + 0.05;
	ALBEDO = vec3(0.05, y, 0);
}
