shader_type spatial;

uniform vec3 Albedo : source_color;
uniform sampler2D Normal;
uniform sampler2D Roughness;
uniform float NormalScale = 10;
uniform float RoughnessScale = 1;

void fragment() {
	// Place fragment code here.
	ALBEDO = Albedo;
	NORMAL_MAP = texture(Normal, UV*NormalScale).rgb;
	ROUGHNESS = texture(Roughness, UV*RoughnessScale).g;
	METALLIC = 1.0;
	SPECULAR = 0.5;
}
