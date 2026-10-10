use Cwd qw(abs_path);
use File::Basename qw(dirname);

my $y2k_config = dirname(dirname(abs_path(__FILE__))) . '/.latexmkrc';
do $y2k_config or die "Cannot load $y2k_config: $@ $!\n";
