% fmf_temp_file.mp -- do not edit, generated automatically by vec_dm_born.tex
input feynmp
require_RCS_revision "1.30";
beginchar(1, 150*1.0pt#, 75*1.0pt#, 0);
"feynmf: 1";
LaTeX_unitlength:=1.0pt;
subgraph (0, 0, w, h);
vinit;
pickup pencircle scaled thin;
vright (__o1, __o2);
vleft (__i1, __i2);
vlabel ("$\bar {\psi },\bar {q}$", __o1);
vlabel ("$\psi ,q$", __o2);
vlabel ("$\bar {q}$", __i2);
vlabel ("$q$", __i1);
vlabel ("$g_{q}$", __v1);
vlabel ("$g_{\textsc {dm}},g_{q}$", __v2);
vconnect ("quark", __o1, __v2);
vconnect ("boson, label=$Z'$", __v1, __v2);
vconnect ("quark", __v2, __o2);
vconnect ("quark", __i1, __v1);
vconnect ("quark", __v1, __i2);
vdot (__v1, __v2);
vfreeze;
vdraw;
endsubgraph;
endchar;
% the end.
end.
endinput;
