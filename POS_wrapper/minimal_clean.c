/*****
The MIT License (MIT)
Copyright © 2020 <copyright holders>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

****/

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <assert.h>


#define DEFAULT_OUTPUT "cleaned"
#define MAX_LEX_STRING 2000
#define PERIOD_DELIM_STR " . "
#define MAX_LEX_STRING_DELIMITED (MAX_LEX_STRING*sizeof(PERIOD_DELIM_STR))

char *clone_string(char *inp)
{
    char *ret_val = NULL;
    if (inp)
    {
        ret_val = malloc(strlen(inp) + 1);
        strcpy(ret_val,inp);
    }
    return ret_val;
}


int ArgPos(char *str, int argc, char **argv) {
  int a;
  for (a = 1; a < argc; a++) if (!strcmp(str, argv[a])) {
    if (a == argc - 1) {
      printf("Argument missing for %s\n", str);
      exit(1);
    }
    return a;
  }
  return -1;
}



static
int
is_number_term(char *buffer,int index,int len)
{
    if (index == 0 || index + 1 >= len )
        return 0;
    if (isdigit(buffer[index-1]) && isdigit(buffer[index+1]))
        return 1;
    return 0;
}

static 
void
expand_punctuation_impl(char *punct_arr,int arr_len,char *buffer,int max_len,char *delim_word,int len,int limit)
{
    int index = 0;
    int delim_index = 0;
    for (index = 0; index < len; index++)
    {
        int found =  0;
        for (int j = 0; j < arr_len; j++)
        {
            if (buffer[index] == punct_arr[j] && (buffer[index] != ',' || !is_number_term(buffer,index,len)))
            {
                char delimiter[10];
                sprintf(delimiter," %c ",buffer[index]);
                //printf("Copying :%s:\n",delimiter);
                strcpy(&delim_word[delim_index],delimiter);
                delim_index += strlen(delimiter);
                found = 1;
                break;
            }
        }
        if (!found)
            delim_word[delim_index++] = buffer[index];
    }
    delim_word[delim_index] = 0;
    assert(delim_index < limit);
}

static char punctuations[] = { ',',':',';','[',']','{','}','(',')','!','?','/','%'};
void
expand_punctuation(char *buffer,int max_len,char *delim_word,int len,int limit)
{
        expand_punctuation_impl(punctuations,sizeof(punctuations),buffer,max_len,delim_word,len,limit);
}

static char addl_punctuations[] = { '$','>','<','='};

void
expand_addl_punctuation(char *buffer,int max_len,char *delim_word,int len,int limit)
{
        expand_punctuation_impl(addl_punctuations,sizeof(addl_punctuations),buffer,max_len,delim_word,len,limit);
}

static char bichar_punctuations1[] = { '!', '>','<','=','=','='};
static char bichar_punctuations2[] = { '=','=','=','=','<','>'};

void normalize_inequalities(char *buffer,int max_len,char *delim_word,int len,int limit)
{
    int index = 0;
    int delim_index = 0;
    int arr_len  = sizeof(bichar_punctuations1); 
    int second_char_offset = 3;
    for (index = 0; index < len; index++)
    {
        int found =  0;
        for (int j = 0; j < arr_len; j++)
        {
            
            if (index + second_char_offset < len && buffer[index] == bichar_punctuations1[j] && buffer[index + second_char_offset] == bichar_punctuations2[j])
            {
                char delimiter[10];
                sprintf(delimiter," %c%c ",buffer[index],buffer[index+second_char_offset]);
                //printf("Copying :%s:\n",delimiter);
                strcpy(&delim_word[delim_index],delimiter);
                delim_index += strlen(delimiter);
                buffer[index+second_char_offset] = ' ';
                found = 1;
                break;
            }
        }
        if (!found)
            delim_word[delim_index++] = buffer[index];
    }
    delim_word[delim_index] = 0;
    assert(delim_index < limit);
}



// Reads a single word from a file, assuming space + tab + EOL to be word boundaries
int ReadWord(char *word, FILE *fin,int lowercase) 
{
  int a = 0, ch;
  while (!feof(fin)) 
  {
    ch = fgetc(fin);
    if (ch == 13) continue;
    if ((ch == ' ') || (ch == '\t') || (ch == '\n')) 
    {
      if (a > 0) {
        if (ch == '\n') ungetc(ch, fin);
        break;
      }
      if (ch == '\n') 
      {
        strcpy(word, (char *)"\n");
        return 1;
      } else continue;
    }
    word[a] = lowercase ? tolower(ch) :  ch;
    a++;
    if (a >= MAX_LEX_STRING - 1) a--;   // Truncate too long words
  }
  word[a] = 0;
  return 0;
}



int clean_impl(char *buffer,int max_len,char replace_char,char *delim_word)
{
    int index = 0;
    int len = strlen(buffer);
    char mod_word[MAX_LEX_STRING_DELIMITED];
    expand_punctuation(buffer,max_len,delim_word,len,MAX_LEX_STRING_DELIMITED);
    strcpy(mod_word,delim_word);
    len = strlen(mod_word);
    expand_addl_punctuation(mod_word,max_len,delim_word,len,MAX_LEX_STRING_DELIMITED);
    strcpy(mod_word,delim_word);
    len = strlen(mod_word);
    normalize_inequalities(mod_word,max_len,delim_word,len,MAX_LEX_STRING_DELIMITED);
    return 0;
}





void *minimal_clean(char *train_file,char *output_file,int lowercase) 
{
  clock_t now;
  char tmp_file[MAX_LEX_STRING];
  sprintf(tmp_file,"%s",output_file);

  FILE *fo = fopen(tmp_file, "w");
  FILE *fi = fopen(train_file, "rb");
  if (!fi)
  {
      fprintf(stderr,"Unable to open input file %s\n",train_file);
      exit(-2);
  } 
  if (!fo)
  {
      fprintf(stderr,"Unable to open output file %s\n",output_file);
      exit(-3);
  } 
  int is_nl = 0;
  while (1) 
  {
        char word[MAX_LEX_STRING];
        char delimited_word[MAX_LEX_STRING_DELIMITED];
        word[0] = delimited_word[0] = 0;
        is_nl = ReadWord(word,fi,lowercase);
        int len = strlen(word);
        clean_impl(word,MAX_LEX_STRING,' ',delimited_word);
        if (feof(fi)) break;
        fprintf(fo,"%s",delimited_word);
        if (!is_nl)
            fprintf(fo," ");
        //printf("In thread %'lld, word :%s: \n",(long long)id, (is_nl? "NL": word));
  }// end main while loop
  fclose(fi);
  fclose(fo);
}






int main(int argc, char **argv) 
{
  int i;
  char *train_file = NULL, *output_file = NULL;
  int lowercase = 0;

  if (argc == 1) {
    printf("minimal  text cleaning (BERT corpus pre-preprocessing)\n\n");
    printf("Purely performs space addition to separate punctuations from text honoring terms like 123,5679 \n\n");
    printf("Parameters for input:\n");
    printf("\t-input <file>\n");
    printf("\t\tUse input data from <file> to clean\n");
    printf("\t-lowercase 0/1 [%d] <file>\n",lowercase);
    printf("\t\tConvert to lowercase\n");
    printf("\t-output <file>\n");
    printf("\t\tUse <file> to save the cleaned data \n");
    printf("./minimal_clean -input data.txt -output cleaned.txt  -lowercase 1\n\n");
    return 0;
  }
  output_file = NULL;
  if ((i = ArgPos((char *)"-lowercase", argc, argv)) > 0) lowercase = atoi(argv[i + 1]);
  if ((i = ArgPos((char *)"-input", argc, argv)) > 0) train_file = clone_string(argv[i + 1]);
  if ((i = ArgPos((char *)"-output", argc, argv)) > 0) output_file = clone_string( argv[i + 1]);
  if (output_file == NULL)
      output_file = clone_string(DEFAULT_OUTPUT);
  
  printf("Starting to clean file \n");
  fflush(stdout);
  minimal_clean(train_file,output_file,lowercase);
  printf("cleaning complete \n");
  fflush(stdout);
  return 0;
}

