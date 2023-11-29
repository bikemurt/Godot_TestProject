shader_type spatial;
render_mode blend_mix, depth_draw_opaque, cull_back, diffuse_lambert, specular_schlick_ggx;

uniform sampler2D Albedo1 : source_color;
uniform sampler2D Albedo2 : source_color;
uniform sampler2D MetalRough1;
uniform sampler2D MetalRough2;
uniform sampler2D Normal1;
uniform sampler2D Normal2;

uniform sampler2D BlendMap;

uniform float SpecularFac;
uniform bool MixSpecular;
uniform float SpecBlendOffset;
uniform float SpecBlendScale;

uniform float UVFactor1 = 1;
uniform float UVFactor2 = 1;

void fragment() {
	
	vec2 UVx1 = UV * UVFactor1;
	vec2 UVx2 = UV * UVFactor2;
	
	vec3 factor = texture(BlendMap, UV2).xxx;
	
	vec3 a1 = texture(Albedo1, UVx1).xyz;
	vec3 a2 = texture(Albedo2, UVx2).xyz;
	
	vec3 m1 = texture(MetalRough1, UVx1).xyz;
	vec3 m2 = texture(MetalRough2, UVx2).xyz;

	vec3 r1 = texture(MetalRough1, UVx1).xyz;
	vec3 r2 = texture(MetalRough2, UVx2).xyz;
	
	vec3 n1 = texture(Normal1, UVx1).xyz;
	vec3 n2 = texture(Normal2, UVx2).xyz;
	
	ALBEDO = mix(a1, a2, factor);
	ROUGHNESS = mix(r1, r2, factor).y;
	METALLIC = mix(m1, m2, factor).z;
	NORMAL_MAP = mix(n1, n2, factor);
	
	float specBlendFac = SpecularFac;
	
	if (MixSpecular)
	{
		specBlendFac = SpecularFac * (SpecBlendOffset + SpecBlendScale * factor.x);
	}
	
	SPECULAR = clamp(specBlendFac * SpecularFac, 0.0, 1.0);
}
