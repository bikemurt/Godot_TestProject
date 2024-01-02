shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_lambert, specular_schlick_ggx;

uniform sampler2D AlbedoRough1 : source_color;
uniform sampler2D AlbedoRough2 : source_color;
uniform sampler2D AlbedoRough3 : source_color;
uniform sampler2D Normal1;
uniform sampler2D Normal2;
uniform sampler2D Normal3;

uniform sampler2D BlendMap;

uniform float UVFactor1 = 10;
uniform float UVFactor2 = 10;
uniform float UVFactor3 = 10;

uniform float Metal1 = 0.0;
uniform float Metal2 = 0.0;
uniform float Metal3 = 0.0;

uniform float Spec1 = 0.0;
uniform float Spec2 = 0.0;
uniform float Spec3 = 0.0;

void fragment() {
	vec2 UVx1 = UV * UVFactor1;
	vec2 UVx2 = UV * UVFactor2;
	vec2 UVx3 = UV * UVFactor3;
	
	vec3 factor = texture(BlendMap, UV).rgb;
	
	vec3 a1 = texture(AlbedoRough1, UVx1).rgb;
	vec3 a2 = texture(AlbedoRough2, UVx2).rgb;
	vec3 a3 = texture(AlbedoRough3, UVx3).rgb;
	
	float r1 = texture(AlbedoRough1, UVx1).a;
	float r2 = texture(AlbedoRough2, UVx2).a;
	float r3 = texture(AlbedoRough3, UVx3).a;
	
	vec3 n1 = texture(Normal1, UVx1).rgb;
	vec3 n2 = texture(Normal2, UVx2).rgb;
	vec3 n3 = texture(Normal3, UVx3).rgb;
	
	
	vec3 albedo_1 = mix(a1, a2, factor.r);
	float rough_1 = mix(r1, r2, factor.r);
	float metal_1 = mix(Metal1, Metal2, factor.r);
	float spec_1 = mix(Spec1, Spec2, factor.r);
	vec3 normal_1 = mix(n1, n2, factor.r);
	
	vec3 albedo_2 = mix(albedo_1, a3, factor.g);
	float rough_2 = mix(rough_1, r3, factor.g);
	float metal_2 = mix(metal_1, Metal3, factor.g);
	float spec_2 = mix(spec_1, Spec3, factor.g);
	vec3 normal_2 = mix(normal_1, n3, factor.g);
	
	//vec3 c = 0.3 * COLOR.rgb;
	//vec3 r_mix = mix(orig_color, vec3(1,0,0), c.r);
	//vec3 g_mix = mix(r_mix, vec3(0,1,0), c.g);
	//vec3 b_mix = mix(g_mix, vec3(0,0,1), c.b);
	
	//ALBEDO = b_mix;
	
	ALBEDO = albedo_2;
	ROUGHNESS = rough_2;
	METALLIC = metal_2;
	SPECULAR = spec_2;
	NORMAL_MAP = normal_2;
}
