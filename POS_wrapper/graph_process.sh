set -x
sentence=${1?"Enter sentence"}
to_lower=${2-0}
bigram_gen=${3-1}
tmp_file=tmp$$
tmp_file2=tmp2$$
pass1_tmp_file=pass1_$$
#echo "$sentence"
python conv_unicode.py "$sentence" > $tmp_file
#cat $tmp_file > arg
SERVER_URL=`python get_config.py`
#cat arg
#./minimal_clean -lowercase $to_lower  -input $tmp_file -output $tmp_file2 > /dev/null
cp $tmp_file $tmp_file2
sentence=`cat $tmp_file2`
cp $tmp_file2 out_minimal_pre
wget $SERVER_URL"$sentence" -O $tmp_file 2>/dev/null
#cp $tmp_file pass1
cp $tmp_file $pass1_tmp_file
if [ $bigram_gen -ne 0 ]
then
	python simple_phrase_gen.py $tmp_file pos_stopwords.txt 100 > $tmp_file2
	#cp $tmp_file2 pass2
	sentence=`head -1 $tmp_file2`
	#echo "$sentence"
	wget $SERVER_URL"$sentence" -O $tmp_file 2>/dev/null
	#cp $tmp_file pass3
	python simple_phrase_gen.py $tmp_file pos_stopwords.txt 100 | head -1 > $tmp_file2
	#cp $tmp_file2 pass4
	sentence=`head -1 $tmp_file2`
	wget $SERVER_URL"$sentence" -O $tmp_file 2>/dev/null
	cat $tmp_file2
	cat $tmp_file
	echo "-------"
fi
cat $pass1_tmp_file
rm -f $tmp_file $tmp_file2 $pass1_tmp_file out_minimal_pre
