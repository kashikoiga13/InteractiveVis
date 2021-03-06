%-----------------------------------------------------------------------
% Job saved on 28-Apr-2021 18:22:15 by cfg_util (rev $Rev: 7345 $)
% spm SPM - SPM12 (7487)
% cfg_basicio BasicIO - Unknown
%-----------------------------------------------------------------------
matlabbatch{1}.spm.util.imcalc.input = {'C:\Users\DZNE\ADNI_Daten\aal\aal.nii,1'};
matlabbatch{1}.spm.util.imcalc.output = 'aal_cerebellum.nii';
matlabbatch{1}.spm.util.imcalc.outdir = {'C:\Users\DZNE\ADNI_Daten\Hippocampus_masks'};
matlabbatch{1}.spm.util.imcalc.expression = 'i1>=91';
matlabbatch{1}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{1}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{1}.spm.util.imcalc.options.mask = 0;
matlabbatch{1}.spm.util.imcalc.options.interp = 0;
matlabbatch{1}.spm.util.imcalc.options.dtype = 2;
matlabbatch{2}.spm.util.imcalc.input = {'C:\Users\DZNE\ADNI_Daten\aal\aal.nii,1'};
matlabbatch{2}.spm.util.imcalc.output = 'aal_temporal.nii';
matlabbatch{2}.spm.util.imcalc.outdir = {'C:\Users\DZNE\ADNI_Daten\Hippocampus_masks'};
matlabbatch{2}.spm.util.imcalc.expression = '((i1>=37).*(i1<=42)) + (i1==55) +( i1==56) + ((i1>=79).*(i1<=90))';
matlabbatch{2}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{2}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{2}.spm.util.imcalc.options.mask = 0;
matlabbatch{2}.spm.util.imcalc.options.interp = 0;
matlabbatch{2}.spm.util.imcalc.options.dtype = 2;
matlabbatch{3}.spm.util.imcalc.input = {'C:\Users\DZNE\ADNI_Daten\aal\aal.nii,1'};
matlabbatch{3}.spm.util.imcalc.output = 'aal_insula_cingulate.nii';
matlabbatch{3}.spm.util.imcalc.outdir = {'C:\Users\DZNE\ADNI_Daten\Hippocampus_masks'};
matlabbatch{3}.spm.util.imcalc.expression = '((i1>=29).*(i1<=36))';
matlabbatch{3}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{3}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{3}.spm.util.imcalc.options.mask = 0;
matlabbatch{3}.spm.util.imcalc.options.interp = 0;
matlabbatch{3}.spm.util.imcalc.options.dtype = 2;
matlabbatch{4}.spm.util.imcalc.input = {'C:\Users\DZNE\ADNI_Daten\aal\aal.nii,1'};
matlabbatch{4}.spm.util.imcalc.output = 'aal_frontal.nii';
matlabbatch{4}.spm.util.imcalc.outdir = {'C:\Users\DZNE\ADNI_Daten\Hippocampus_masks'};
matlabbatch{4}.spm.util.imcalc.expression = '((i1>=1).*(i1<=28)) + (i1==69) + (i1==70)';
matlabbatch{4}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{4}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{4}.spm.util.imcalc.options.mask = 0;
matlabbatch{4}.spm.util.imcalc.options.interp = 0;
matlabbatch{4}.spm.util.imcalc.options.dtype = 2;
matlabbatch{5}.spm.util.imcalc.input = {'C:\Users\DZNE\ADNI_Daten\aal\aal.nii,1'};
matlabbatch{5}.spm.util.imcalc.output = 'aal_occipital.nii';
matlabbatch{5}.spm.util.imcalc.outdir = {'C:\Users\DZNE\ADNI_Daten\Hippocampus_masks'};
matlabbatch{5}.spm.util.imcalc.expression = '((i1>=43).*(i1<=54))';
matlabbatch{5}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{5}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{5}.spm.util.imcalc.options.mask = 0;
matlabbatch{5}.spm.util.imcalc.options.interp = 0;
matlabbatch{5}.spm.util.imcalc.options.dtype = 2;
matlabbatch{6}.spm.util.imcalc.input = {'C:\Users\DZNE\ADNI_Daten\aal\aal.nii,1'};
matlabbatch{6}.spm.util.imcalc.output = 'aal_parietal.nii';
matlabbatch{6}.spm.util.imcalc.outdir = {'C:\Users\DZNE\ADNI_Daten\Hippocampus_masks'};
matlabbatch{6}.spm.util.imcalc.expression = '((i1>=57).*(i1<=68))';
matlabbatch{6}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{6}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{6}.spm.util.imcalc.options.mask = 0;
matlabbatch{6}.spm.util.imcalc.options.interp = 0;
matlabbatch{6}.spm.util.imcalc.options.dtype = 2;
matlabbatch{7}.spm.util.imcalc.input = {'C:\Users\DZNE\ADNI_Daten\aal\aal.nii,1'};
matlabbatch{7}.spm.util.imcalc.output = 'aal_basal_ganglia.nii';
matlabbatch{7}.spm.util.imcalc.outdir = {'C:\Users\DZNE\ADNI_Daten\Hippocampus_masks'};
matlabbatch{7}.spm.util.imcalc.expression = '((i1>=71).*(i1<=78))';
matlabbatch{7}.spm.util.imcalc.var = struct('name', {}, 'value', {});
matlabbatch{7}.spm.util.imcalc.options.dmtx = 0;
matlabbatch{7}.spm.util.imcalc.options.mask = 0;
matlabbatch{7}.spm.util.imcalc.options.interp = 0;
matlabbatch{7}.spm.util.imcalc.options.dtype = 2;
