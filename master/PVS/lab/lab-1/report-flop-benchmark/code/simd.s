.LBB110_207:
	addps	%xmm3, %xmm0
	mulps	%xmm3, %xmm0
	addps	%xmm3, %xmm0
	movaps	%xmm3, %xmm1
	mulps	%xmm0, %xmm1
	movaps	%xmm0, %xmm2
	movaps	%xmm1, %xmm0
	addl	$-2, %eax
	jne	.LBB110_207
.LBB110_208:
