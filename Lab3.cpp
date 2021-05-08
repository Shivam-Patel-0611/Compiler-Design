#include<iostream>
#include<fstream>
#include<ctype.h>
#include<bits/stdc++.h>
using namespace std;

string keywords[32] = {"auto","break","case","char","const","continue","default","do","double","else","enum","extern","float","for","goto","if","int","long","register","return"
"short","signed","sizeof","static","struct","switch","typedef","union","unsigned","void","volatile","while"};

char operators[6] = {'+','-','*','/','%','='};

char separators[8] = {';',',','[',']','(',')','{','}'};

bool isoperator(string c){
    for(int i=0;i<6;i++){
        if(c[0]==operators[i]){
            return true;
        }
    }
    return false;
}

bool iskeyword(string s){
    for(int i=0;i<32;i++){
        int x = s.compare(keywords[i]);
        if(x==0)
            return true;
    }
    return false;
}

bool isseparator(string s){
    for(int i=0;i<8;i++){
        if(s[0]==separators[i])
            return true;
    }
    return false;
}

bool isnumber(string s){
    for(int i=0;i<s.length();i++){
        if(!isdigit(s[i]))
            return false;
    }
    return true;
}

int main(){
    fstream file;
    file.open("test.c",ios::in);
    if(!file){
        cout<<"\nOops!!!Error opening th file"<<endl;
    }
    else{
        cout<<"\nVoila!!!! File successfully opened for analysis\n"<<endl;
    }

    ofstream out;
    out.open("output.c");
    if(!out){
        cout<<"\nOops!!!Error opening th file"<<endl;
    }
    else{
        cout<<"\nVoila!!!! File successfully opened for writing\n"<<endl;
    }
    
    string s = "";
    string s1 = "";
    string literals="";
    string header="";
    string line;
    string digit;
    string variable;
    string symbols;
    
    char c,c1;
    
    int i;
    int flag;
    int flag1;
    int flag2;
    int flag3=0;
    
    while(getline(file,line)){
        //cout<<line<<endl;
        /*for(int i=0;i<line.length();i++){
            cout<<line[i]<<endl;
        }*/
        digit="";
        variable="";
        symbols="";
        i=0;
        flag=0;
        flag1=0;
        flag2=0;  
        if(line.length()==1)
        {
            s+=" "+line;
            s1+=" "+line;
        }
        else{
            while(i<=line.length()-1){ 
            
                if(i==line.length()-1)
                    c=c1;
                else{
                    c = line[i];
                    c1 = line[i+1];
                }

                // This part is to match the multi-line comments or to find the singlr line comments
                if(flag3==1)
                {
                    if(c=='*' && c1=='/'){
                        flag3=0;
                    }
                }
                else if(c=='/' && c1=='/')
                {
                    i=line.length();
                }
                else if(c=='/' && c1=='*')
                {
                    flag3=1;
                }
                // This part is for checking the literals
                else if(c=='\"')
                {
                    i++;
                    string temp = "";
                    while(line[i]!='\"' && i<line.length())
                    {
                        //literals+=line[i];
                        temp+=line[i];
                        i++;
                    }
                    i++;
                    literals+=temp;
                    s1+=" \""+temp+"\";";
                    literals+=" ";
                }
                else if(c=='#')
                {
                    string temp = line;
                    header+=" "+temp;
                    s1+=temp;
                    i=line.length();
                }
                // This part starts checking for varible, digits, symbols
                else if(isdigit(c)){
                    if(flag1==0 && flag==0)
                        digit+=c;
                    if(flag1==0 && flag==1)
                        variable+=c;
                    //cout<<c<<endl;
                }
                else if(isalpha(c)){
                    if(flag1==0 && flag==0){
                        flag=1;
                        variable+=digit;
                        digit="";
                    }
                    variable+=c;
                    //cout<<variable<<endl;
                }
                else if(!isspace(c)){
                    symbols+=c;
                    flag2=1;
                }
                
                if(i==line.length()-1 || flag1==1 || flag2==1)
                {
                    if(digit.length()!=0 && flag==0){
                        s1+=" "+digit;
                        s+=" "+digit;
                        literals+=digit+" ";
                    }
                    if(variable.length()!=0){
                        s+=" "+variable;
                        s1+=" "+variable;
                    }
                    if(flag2==1){
                        s+=" "+symbols;
                        s1+=" "+symbols;
                    }
                    //cout<<s<<endl;
                    flag2=0;
                    flag1=0;
                    flag=0;
                    digit="";
                    variable="";
                    symbols="";
                }
                if(isspace(c1)){
                    flag1=1;
                }
                i++; 
            }
        }
        //cout<<s1<<endl;
        if(s1.length()!=0)
            out<<s1<<endl;
        s1="";       
    }
    //cout<<"The String separated will be : \n\nAns :  "<<s<<endl;
    file.close();
    cout<<endl;

    // Below is the code to print all the stuff
    istringstream stream(s);
    string word;
    set<string> storage;
    while(stream>>word){
        storage.insert(word);
    }

    istringstream stream1(literals);
    set<string> storage1;
    while(stream1>>word){
        storage1.insert(word);
    }

    istringstream stream2(header);
    set<string> storage2;
    while(stream2>>word){
        storage2.insert(word);
    }

    cout<<"The Total Tokens are : "<<storage.size()+storage1.size()+storage2.size()<<endl;
    cout<<endl;

    for(auto it = storage.begin();it!=storage.end();it++){
        if(isoperator(*it))
            cout<<*it<<"\t : \toperator"<<endl;
        else if(iskeyword(*it))
            cout<<*it<<"\t : \tkeyword"<<endl;
        else if(isseparator(*it))
            cout<<*it<<"\t : \tseparator"<<endl;
        /*else if(isnumber(*it))
            cout<<"hello"<<endl;
            //storage1.insert(*it);
            //literals+=*it+" ";
        */
       else
            cout<<*it<<"\t : \tIdentifier"<<endl;
    }
    
    for(auto it = storage1.begin();it!=storage1.end();it++){
        cout<<*it<<"\t : \tLiterals"<<endl;
    }

    for(auto it = storage2.begin();it!=storage2.end();it++){
        cout<<*it<<"\t : \theader"<<endl;
    }
    return 0;
}