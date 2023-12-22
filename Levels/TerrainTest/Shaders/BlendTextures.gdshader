shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_lambert, specular_schlick_ggx;

uniform sampler2D AlbedoRough1 : source_color;
uniform sampler2D AlbedoRough2 : source_color;
uniform sampler2D Normal1;
uniform sampler2D Normal2;

uniform sampler2D BlendMap;

uniform float UVFactor1 = 10;
uniform float UVFactor2 = 10;

uniform float Metal1 = 0.0;
uniform float Metal2 = 0.0;

uniform float Spec1 = 0.0;
uniform float Spec2 = 0.0;

void fragment() {
	vec2 UVx1 = UV * UVFactor1;
	vec2 UVx2 = UV * UVFactor2;
	
	vec3 factor = texture(BlendMap, UV).xxx;
	
	vec3 a1 = texture(AlbedoRough1, UVx1).xyz;
	vec3 a2 = texture(AlbedoRough2, UVx2).xyz;
	
	float r1 = texture(AlbedoRough1, UVx1).w;
	float r2 = texture(AlbedoRough2, UVx2).w;
	
	vec3 n1 = texture(Normal1, UVx1).xyz;
	vec3 n2 = texture(Normal2, UVx2).xyz;
	
	ALBEDO = mix(a1, a2, factor);
	ROUGHNESS = mix(r1, r2, factor.r);
	METALLIC = mix(Metal1, Metal2, factor.r);
	SPECULAR = mix(Spec1, Spec2, factor.r);
	NORMAL_MAP = mix(n1, n2, factor);
}
