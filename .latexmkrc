use Cwd qw(abs_path);
use File::Basename qw(dirname);

my $y2k_root = dirname(abs_path(__FILE__));
$ENV{TEXINPUTS} = join(':', $y2k_root, "$y2k_root/assets/fonts",
    "$y2k_root/build/assets", "$y2k_root/examples", $ENV{TEXINPUTS} // '', '');
$out_dir = "$y2k_root/build";
$pdf_mode = 1;
