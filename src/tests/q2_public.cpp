#define main aim_embedded_public_main
#include "../main/A1_q2.cpp"
#undef main

int main() {
    try {
        { std::vector<aim::q2::Damage> r=clean({"2 5","bad","2 9","1 3"}); CHECK(r.size()==2 && r[0].id==2 && r[0].value==5 && r[1].id==1); }
        { CHECK(clean({}).empty()); }
    } catch(const std::exception& e) {
        std::cerr << e.what() << "\n";
        return 1;
    }
    return 0;
}
