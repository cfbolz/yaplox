import sys
from rpython import conftest

from yaplox.yaplox_return_exception import YaploxReturnException



class o:
    view = False
    viewloops = True
conftest.option = o

from rpython.rlib.nonconst import NonConstant
from rpython.rlib import jit
from rpython.jit.metainterp.test.test_ajit import LLJitMixin

from yaplox.main import Yaplox
from yaplox import obj


class TestLLtype(LLJitMixin):
    def run_string(self, source):
        y = Yaplox()
        program = y.uptoresolve(source)
        def interp_w():
            obj.W_String("abc")
            YaploxReturnException(obj.w_nil)
            jit.set_param(None, "disable_unrolling", 5000)
            y.interpreter.interpret(program, on_error=y.runtime_error)

        interp_w()  # check that it runs

        y = Yaplox()
        program = y.uptoresolve(source)

        self.meta_interp(interp_w, [], listcomp=True, listops=True, backendopt=True, inline=True)

    def test_loop(self):
        self.run_string("""
fun main(start) {
    var xyz = start;

    while (xyz < 10000) {
      xyz = xyz + 1;
    }
}

main(0);
""")

    def test_loop_global(self):
        self.run_string("""
var xyz = 0;

while (xyz < 10000) {
  xyz = xyz + 1;
}
""")

    def test_loop_funcall(self):
        self.run_string("""
fun inc(x) {
    return x + 1;
}
fun main() {
    var xyz = 0;

    while (xyz < 10000) {
      xyz = inc(xyz);
    }
}


main();
""")

    def test_loop_create_instance(self):
        self.run_string("""
class Inc {
    init(x) {
        this.val = x + 1;
    }
    getf() {
        return this.val;
    }
}
fun main() {
    var xyz = 0;

    while (xyz < 10000) {
      xyz = Inc(xyz).getf();
    }
}

main();
""")

    def test_loop_access_instance(self):
        self.run_string("""
class Inc {
    init(x) {
        this.incr = x;
    }
    getf() {
        return this.incr;
    }
}
fun main() {
    var xyz = 0;
    var inst = Inc(1);

    while (xyz < 10000) {
      xyz = inst.getf() + xyz;
    }
}

main();
""")


    def test_squareroot(self):
        self.run_string("""
fun abs(x) {
    if (x >= 0) {
        return x;
    } else {
        return -x;
    }
}
fun squareroot(x) {
    var guess = x;
    while (abs(guess * guess - x) > 0.00000001) {
        guess = (guess + x / guess) / 2;
    }
    return guess;
}
fun main() {
    for (var i = 0; i <= 100; i = i + 1) {
      print i;
      print squareroot(i);
    }
}

main();
""")


    def test_linked(self):
        self.run_string("""
class Terminator {
    isend () { return true; }
}
class Node {
    init(data) {
        this.prev = Terminator();
        this.next = Terminator();
        this.data = data;
    }
    isend () { return false; }
}

class List {
    init() {
        this._len = 0;
        this.head = Terminator();
        this.tail = Terminator();
    }

    len() {
        return this._len;
    }

    get_item(n) {
        var i = 0;
        var node = this.head;

        while (!node.isend()) {
            if (i == n)
                return node.data;

            i = i + 1;
            node = node.next;
        }
    }

    pop() {
        if (this.tail.isend())
            return;

        var node  = this.tail;
        this.tail = node.prev;

        if (!this.tail.isend())
            this.tail.next = Terminator();
        else
            this.head = Terminator();

        this._len = this._len - 1;
        return node.data;
    }

    push(data) {
        var node = Node(data);

        if (this.head.isend()) {
            this.head = node;
            this.tail = node;
        } else {
            node.prev = this.tail;
            this.tail.next = node;
            this.tail = node;
        }

        this._len = this._len + 1;
    }
}

fun main() {
    var list = List();

    for (var i = 0; i < 200; i = i + 1) {
        list.push(i);
    }

    list.pop();
    list.pop();

    for (var i = 0; i < list._len; i = i + 1) {
        print list.get_item(i); // i'm sorry
    }
}

main();
""")
