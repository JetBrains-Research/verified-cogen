#![feature(box_patterns)]
#![feature(ptr_metadata)]
#![feature(never_type)]
#![feature(allocator_api)]
#![allow(non_camel_case_types)]
#![allow(unused_imports)]
#![allow(unused_variables)]
#![allow(unused_assignments)]
#![allow(unreachable_patterns)]
#![allow(unused_parens)]
#![allow(unused_braces)]
#![allow(dead_code)]
#![allow(unreachable_code)]
#![allow(unconditional_recursion)]
#![allow(unused_mut)]
#![allow(unused_labels)]
use std::marker::PhantomData;
use std::rc::Rc;
use std::sync::Arc;
use std::alloc::Allocator;
use std::alloc::Global;
use std::mem::ManuallyDrop;
use std::ptr::Pointee;
use std::ptr::Thin;
fn op<A, B>(a: A) -> B { panic!() }
fn static_ref<T>(t: T) -> &'static T { panic!() }
fn tracked_new<T>(t: T) -> Tracked<T> { panic!() }
fn tracked_exec_borrow<'a, T>(t: &'a T) -> &'a Tracked<T> { panic!() }
fn clone<T>(t: &T) -> T { panic!() }
fn rc_new<T>(t: T) -> std::rc::Rc<T> { panic!() }
fn arc_new<T>(t: T) -> std::sync::Arc<T> { panic!() }
fn box_new<T>(t: T) -> Box<T> { panic!() }
struct Tracked<A> { a: PhantomData<A> }
impl<A> Tracked<A> {
    pub fn get(self) -> A { panic!() }
    pub fn borrow(&self) -> &A { panic!() }
    pub fn borrow_mut(&mut self) -> &mut A { panic!() }
}
struct Ghost<A> { a: PhantomData<A> }
impl<A> Clone for Ghost<A> { fn clone(&self) -> Self { panic!() } }
impl<A> Copy for Ghost<A> { }
impl<A: Copy> Clone for Tracked<A> { fn clone(&self) -> Self { panic!() } }
impl<A: Copy> Copy for Tracked<A> { }
#[derive(Clone, Copy)] struct int;
#[derive(Clone, Copy)] struct nat;
struct FnSpec<Args, Output> { x: PhantomData<(Args, Output)> }
struct InvariantBlockGuard;
fn open_atomic_invariant_begin<'a, X, V>(_inv: &'a X) -> (InvariantBlockGuard, V) { panic!(); }
fn open_local_invariant_begin<'a, X, V>(_inv: &'a X) -> (InvariantBlockGuard, V) { panic!(); }
fn open_invariant_end<V>(_guard: InvariantBlockGuard, _v: V) { panic!() }
fn index<'a, V, Idx, Output>(v: &'a V, index: Idx) -> &'a Output { panic!() }
struct C<const N: usize, A: ?Sized>(Box<A>);
struct Arr<A: ?Sized, const N: usize>(Box<A>);
fn main() {}



trait T58_OptionAdditionalFns<A57_T, > where A57_T : ?Sized,  {
}

enum D29_ControlFlow<A12_B, A13_C, > where A12_B: , A13_C: ,  {
    C33_Continue(
        A13_C,
    ),
    C28_Break(
        A12_B,
    ),
}

impl<A12_B, A13_C, > Clone for D29_ControlFlow<A12_B, A13_C, > where A12_B: Clone, A13_C: Clone,  { fn clone(&self) -> Self { panic!() } }

impl<A12_B, A13_C, > Copy for D29_ControlFlow<A12_B, A13_C, > where A12_B: Copy, A13_C: Copy,  {}

struct D45_Infallible(
);

impl Clone for D45_Infallible { fn clone(&self) -> Self { panic!() } }

impl Copy for D45_Infallible {}

enum D24_Option<A1_T, > where A1_T: ,  {
    C50_None(
    ),
    C25_Some(
        A1_T,
    ),
}

impl<A1_T, > Clone for D24_Option<A1_T, > where A1_T: Clone,  { fn clone(&self) -> Self { panic!() } }

impl<A1_T, > Copy for D24_Option<A1_T, > where A1_T: Copy,  {}

struct D53_ControlFlow<A51_B, A52_C, >(
    Box<A51_B, >,
    Box<A52_C, >,
) where A51_B : ?Sized, A52_C : ?Sized, ;

struct D54_Infallible(
);

struct D56_Option<A55_V, >(
    Box<A55_V, >,
) where A55_V : ?Sized, ;

impl<A57_T, > T58_OptionAdditionalFns<A57_T, > for D56_Option<A57_T, > where A57_T : ?Sized,  {
}

fn f26_fibfib(
    x23_x: u32,
) -> D24_Option<u32, >
{
    match x23_x {
        _ => 
        {
            D24_Option::C25_Some::<u32, >(op::<_, u32>(()), )
        }
        _ => 
        {
            D24_Option::C25_Some::<u32, >(op::<_, u32>(()), )
        }
        _ => 
        {
            D24_Option::C25_Some::<u32, >(op::<_, u32>(()), )
        }
        _ => 
        {
            f37_checked_add(
            match f27_branch::<u32, >(f37_checked_add(
            match f27_branch::<u32, >(f26_fibfib(op::<_, u32>((x23_x, op::<_, u32>(()), )), ), ) {
                D29_ControlFlow::C28_Break { 0: x31_residual, }  => 
                {
                    return f32_from_residual::<u32, >(x31_residual, )
                }
                D29_ControlFlow::C33_Continue { 0: x34_val, }  => 
                {
                    x34_val
                }
            }, 
            match f27_branch::<u32, >(f26_fibfib(op::<_, u32>((x23_x, op::<_, u32>(()), )), ), ) {
                D29_ControlFlow::C28_Break { 0: x35_residual, }  => 
                {
                    return f32_from_residual::<u32, >(x35_residual, )
                }
                D29_ControlFlow::C33_Continue { 0: x36_val, }  => 
                {
                    x36_val
                }
            }, ), ) {
                D29_ControlFlow::C28_Break { 0: x38_residual, }  => 
                {
                    return f32_from_residual::<u32, >(x38_residual, )
                }
                D29_ControlFlow::C33_Continue { 0: x39_val, }  => 
                {
                    x39_val
                }
            }, 
            match f27_branch::<u32, >(f26_fibfib(op::<_, u32>((x23_x, op::<_, u32>(()), )), ), ) {
                D29_ControlFlow::C28_Break { 0: x40_residual, }  => 
                {
                    return f32_from_residual::<u32, >(x40_residual, )
                }
                D29_ControlFlow::C33_Continue { 0: x41_val, }  => 
                {
                    x41_val
                }
            }, )
        }
    }
}

fn f32_from_residual<A1_T, >(
    x44_option: D24_Option<D45_Infallible, >,
) -> D24_Option<A1_T, > where A1_T: , 
{
    panic!()
}

fn f27_branch<A1_T, >(
    x44_option: D24_Option<A1_T, >,
) -> D29_ControlFlow<D24_Option<D45_Infallible, >, A1_T, > where A1_T: , 
{
    panic!()
}

fn f37_checked_add(
    x48_lhs: u32,
    x49_rhs: u32,
) -> D24_Option<u32, >
{
    panic!()
}
