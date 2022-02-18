/* Created by Language version: 7.7.0 */
/* VECTORIZED */
#define NRN_VECTORIZED 1
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "scoplib_ansi.h"
#undef PI
#define nil 0
#include "md1redef.h"
#include "section.h"
#include "nrniv_mf.h"
#include "md2redef.h"
 
#if METHOD3
extern int _method3;
#endif

#if !NRNGPU
#undef exp
#define exp hoc_Exp
extern double hoc_Exp(double);
#endif
 
#define nrn_init _nrn_init__shock2pyr
#define _nrn_initial _nrn_initial__shock2pyr
#define nrn_cur _nrn_cur__shock2pyr
#define _nrn_current _nrn_current__shock2pyr
#define nrn_jacob _nrn_jacob__shock2pyr
#define nrn_state _nrn_state__shock2pyr
#define _net_receive _net_receive__shock2pyr 
#define release release__shock2pyr 
 
#define _threadargscomma_ _p, _ppvar, _thread, _nt,
#define _threadargsprotocomma_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt,
#define _threadargs_ _p, _ppvar, _thread, _nt
#define _threadargsproto_ double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt
 	/*SUPPRESS 761*/
	/*SUPPRESS 762*/
	/*SUPPRESS 763*/
	/*SUPPRESS 765*/
	 extern double *getarg();
 /* Thread safe. No static _p or _ppvar. */
 
#define t _nt->_t
#define dt _nt->_dt
#define initW _p[0]
#define Cdur_nmda _p[1]
#define AlphaTmax_nmda _p[2]
#define Beta_nmda _p[3]
#define Erev_nmda _p[4]
#define gbar_nmda _p[5]
#define Cdur_ampa _p[6]
#define AlphaTmax_ampa _p[7]
#define Beta_ampa _p[8]
#define Erev_ampa _p[9]
#define gbar_ampa _p[10]
#define inmda _p[11]
#define g_nmda _p[12]
#define on_nmda _p[13]
#define W_nmda _p[14]
#define iampa _p[15]
#define g_ampa _p[16]
#define on_ampa _p[17]
#define W_ampa _p[18]
#define pregid _p[19]
#define postgid _p[20]
#define r_nmda _p[21]
#define r_ampa _p[22]
#define t0 _p[23]
#define Dr_nmda _p[24]
#define Dr_ampa _p[25]
#define v _p[26]
#define _g _p[27]
#define _tsav _p[28]
#define _nd_area  *_ppvar[0]._pval
 
#if MAC
#if !defined(v)
#define v _mlhv
#endif
#if !defined(h)
#define h _mlhh
#endif
#endif
 
#if defined(__cplusplus)
extern "C" {
#endif
 static int hoc_nrnpointerindex =  -1;
 static Datum* _extcall_thread;
 static Prop* _extcall_prop;
 /* external NEURON variables */
 /* declaration of user functions */
 static double _hoc_sfunc();
 static int _mechtype;
extern void _nrn_cacheloop_reg(int, int);
extern void hoc_register_prop_size(int, int, int);
extern void hoc_register_limits(int, HocParmLimits*);
extern void hoc_register_units(int, HocParmUnits*);
extern void nrn_promote(Prop*, int, int);
extern Memb_func* memb_func;
 
#define NMODL_TEXT 1
#if NMODL_TEXT
static const char* nmodl_file_text;
static const char* nmodl_filename;
extern void hoc_reg_nmodl_text(int, const char*);
extern void hoc_reg_nmodl_filename(int, const char*);
#endif

 extern Prop* nrn_point_prop_;
 static int _pointtype;
 static void* _hoc_create_pnt(_ho) Object* _ho; { void* create_point_process();
 return create_point_process(_pointtype, _ho);
}
 static void _hoc_destroy_pnt();
 static double _hoc_loc_pnt(_vptr) void* _vptr; {double loc_point_process();
 return loc_point_process(_pointtype, _vptr);
}
 static double _hoc_has_loc(_vptr) void* _vptr; {double has_loc_point();
 return has_loc_point(_vptr);
}
 static double _hoc_get_loc_pnt(_vptr)void* _vptr; {
 double get_loc_point_process(); return (get_loc_point_process(_vptr));
}
 extern void _nrn_setdata_reg(int, void(*)(Prop*));
 static void _setdata(Prop* _prop) {
 _extcall_prop = _prop;
 }
 static void _hoc_setdata(void* _vptr) { Prop* _prop;
 _prop = ((Point_process*)_vptr)->_prop;
   _setdata(_prop);
 }
 /* connect user functions to hoc names */
 static VoidFunc hoc_intfunc[] = {
 0,0
};
 static Member_func _member_func[] = {
 "loc", _hoc_loc_pnt,
 "has_loc", _hoc_has_loc,
 "get_loc", _hoc_get_loc_pnt,
 "sfunc", _hoc_sfunc,
 0, 0
};
#define sfunc sfunc_shock2pyr
 extern double sfunc( _threadargsprotocomma_ double );
 /* declare global and static user variables */
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "Cdur_nmda", "ms",
 "AlphaTmax_nmda", "/ms",
 "Beta_nmda", "/ms",
 "Erev_nmda", "mV",
 "gbar_nmda", "uS",
 "Cdur_ampa", "ms",
 "AlphaTmax_ampa", "/ms",
 "Beta_ampa", "/ms",
 "Erev_ampa", "mV",
 "gbar_ampa", "uS",
 "inmda", "nA",
 "g_nmda", "uS",
 "iampa", "nA",
 "g_ampa", "uS",
 0,0
};
 static double delta_t = 0.01;
 static double r_ampa0 = 0;
 static double r_nmda0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 0,0
};
 static DoubVec hoc_vdoub[] = {
 0,0,0
};
 static double _sav_indep;
 static void nrn_alloc(Prop*);
static void  nrn_init(_NrnThread*, _Memb_list*, int);
static void nrn_state(_NrnThread*, _Memb_list*, int);
 static void nrn_cur(_NrnThread*, _Memb_list*, int);
static void  nrn_jacob(_NrnThread*, _Memb_list*, int);
 static void _hoc_destroy_pnt(_vptr) void* _vptr; {
   destroy_point_process(_vptr);
}
 
static int _ode_count(int);
static void _ode_map(int, double**, double**, double*, Datum*, double*, int);
static void _ode_spec(_NrnThread*, _Memb_list*, int);
static void _ode_matsol(_NrnThread*, _Memb_list*, int);
 
#define _cvode_ieq _ppvar[2]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"shock2pyr",
 "initW",
 "Cdur_nmda",
 "AlphaTmax_nmda",
 "Beta_nmda",
 "Erev_nmda",
 "gbar_nmda",
 "Cdur_ampa",
 "AlphaTmax_ampa",
 "Beta_ampa",
 "Erev_ampa",
 "gbar_ampa",
 0,
 "inmda",
 "g_nmda",
 "on_nmda",
 "W_nmda",
 "iampa",
 "g_ampa",
 "on_ampa",
 "W_ampa",
 "pregid",
 "postgid",
 0,
 "r_nmda",
 "r_ampa",
 0,
 0};
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 29, _prop);
 	/*initialize range parameters*/
 	initW = 10;
 	Cdur_nmda = 16.765;
 	AlphaTmax_nmda = 0.2659;
 	Beta_nmda = 0.008;
 	Erev_nmda = 0;
 	gbar_nmda = 0.0005;
 	Cdur_ampa = 1.421;
 	AlphaTmax_ampa = 3.8142;
 	Beta_ampa = 0.1429;
 	Erev_ampa = 0;
 	gbar_ampa = 0.001;
  }
 	_prop->param = _p;
 	_prop->param_size = 29;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 3, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _net_receive(Point_process*, double*, double);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _shock2pyr_reg() {
	int _vectorized = 1;
  _initlists();
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 1,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 29, 3);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 shock2pyr /home/gjgpb9/LargeScaleBLA/components/mechanisms/x86_64/shock2pyr.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[2], _dlist1[2];
 static int release(_threadargsproto_);
 
/*CVODE*/
 static int _ode_spec1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {int _reset = 0; {
   if ( t0 > 0.0 ) {
     if ( t - t0 < Cdur_nmda ) {
       on_nmda = 1.0 ;
       }
     else {
       on_nmda = 0.0 ;
       }
     if ( t - t0 < Cdur_ampa ) {
       on_ampa = 1.0 ;
       }
     else {
       on_ampa = 0.0 ;
       }
     }
   Dr_nmda = AlphaTmax_nmda * on_nmda * ( 1.0 - r_nmda ) - Beta_nmda * r_nmda ;
   Dr_ampa = AlphaTmax_ampa * on_ampa * ( 1.0 - r_ampa ) - Beta_ampa * r_ampa ;
   g_nmda = gbar_nmda * r_nmda ;
   inmda = W_nmda * g_nmda * ( v - Erev_nmda ) * sfunc ( _threadargscomma_ v ) ;
   g_ampa = gbar_ampa * r_ampa ;
   iampa = W_ampa * g_ampa * ( v - Erev_ampa ) ;
   }
 return _reset;
}
 static int _ode_matsol1 (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
 if ( t0 > 0.0 ) {
   if ( t - t0 < Cdur_nmda ) {
     on_nmda = 1.0 ;
     }
   else {
     on_nmda = 0.0 ;
     }
   if ( t - t0 < Cdur_ampa ) {
     on_ampa = 1.0 ;
     }
   else {
     on_ampa = 0.0 ;
     }
   }
 Dr_nmda = Dr_nmda  / (1. - dt*( ( AlphaTmax_nmda * on_nmda )*( ( ( - 1.0 ) ) ) - ( Beta_nmda )*( 1.0 ) )) ;
 Dr_ampa = Dr_ampa  / (1. - dt*( ( AlphaTmax_ampa * on_ampa )*( ( ( - 1.0 ) ) ) - ( Beta_ampa )*( 1.0 ) )) ;
 g_nmda = gbar_nmda * r_nmda ;
 inmda = W_nmda * g_nmda * ( v - Erev_nmda ) * sfunc ( _threadargscomma_ v ) ;
 g_ampa = gbar_ampa * r_ampa ;
 iampa = W_ampa * g_ampa * ( v - Erev_ampa ) ;
  return 0;
}
 /*END CVODE*/
 static int release (double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) { {
   if ( t0 > 0.0 ) {
     if ( t - t0 < Cdur_nmda ) {
       on_nmda = 1.0 ;
       }
     else {
       on_nmda = 0.0 ;
       }
     if ( t - t0 < Cdur_ampa ) {
       on_ampa = 1.0 ;
       }
     else {
       on_ampa = 0.0 ;
       }
     }
    r_nmda = r_nmda + (1. - exp(dt*(( AlphaTmax_nmda * on_nmda )*( ( ( - 1.0 ) ) ) - ( Beta_nmda )*( 1.0 ))))*(- ( ( ( AlphaTmax_nmda )*( on_nmda ) )*( ( 1.0 ) ) ) / ( ( ( AlphaTmax_nmda )*( on_nmda ) )*( ( ( - 1.0 ) ) ) - ( Beta_nmda )*( 1.0 ) ) - r_nmda) ;
    r_ampa = r_ampa + (1. - exp(dt*(( AlphaTmax_ampa * on_ampa )*( ( ( - 1.0 ) ) ) - ( Beta_ampa )*( 1.0 ))))*(- ( ( ( AlphaTmax_ampa )*( on_ampa ) )*( ( 1.0 ) ) ) / ( ( ( AlphaTmax_ampa )*( on_ampa ) )*( ( ( - 1.0 ) ) ) - ( Beta_ampa )*( 1.0 ) ) - r_ampa) ;
   g_nmda = gbar_nmda * r_nmda ;
   inmda = W_nmda * g_nmda * ( v - Erev_nmda ) * sfunc ( _threadargscomma_ v ) ;
   g_ampa = gbar_ampa * r_ampa ;
   iampa = W_ampa * g_ampa * ( v - Erev_ampa ) ;
   }
  return 0;
}
 
static void _net_receive (_pnt, _args, _lflag) Point_process* _pnt; double* _args; double _lflag; 
{  double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _thread = (Datum*)0; _nt = (_NrnThread*)_pnt->_vnt;   _p = _pnt->_prop->param; _ppvar = _pnt->_prop->dparam;
  if (_tsav > t){ extern char* hoc_object_name(); hoc_execerror(hoc_object_name(_pnt->ob), ":Event arrived out of order. Must call ParallelContext.set_maxstep AFTER assigning minimum NetCon.delay");}
 _tsav = t; {
   t0 = t ;
   } }
 
double sfunc ( _threadargsprotocomma_ double _lv ) {
   double _lsfunc;
  _lsfunc = 1.0 / ( 1.0 + 0.33 * exp ( - 0.06 * _lv ) ) ;
    
return _lsfunc;
 }
 
static double _hoc_sfunc(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  sfunc ( _p, _ppvar, _thread, _nt, *getarg(1) );
 return(_r);
}
 
static int _ode_count(int _type){ return 2;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
     _ode_spec1 (_p, _ppvar, _thread, _nt);
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 2; ++_i) {
		_pv[_i] = _pp + _slist1[_i];  _pvdot[_i] = _pp + _dlist1[_i];
		_cvode_abstol(_atollist, _atol, _i);
	}
 }
 
static void _ode_matsol_instance1(_threadargsproto_) {
 _ode_matsol1 (_p, _ppvar, _thread, _nt);
 }
 
static void _ode_matsol(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
 _ode_matsol_instance1(_threadargs_);
 }}

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  r_ampa = r_ampa0;
  r_nmda = r_nmda0;
 {
   on_nmda = 0.0 ;
   r_nmda = 0.0 ;
   W_nmda = initW ;
   on_ampa = 0.0 ;
   r_ampa = 0.0 ;
   W_ampa = initW ;
   t0 = - 1.0 ;
   }
 
}
}

static void nrn_init(_NrnThread* _nt, _Memb_list* _ml, int _type){
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _tsav = -1e20;
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v = _v;
 initmodel(_p, _ppvar, _thread, _nt);
}
}

static double _nrn_current(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt, double _v){double _current=0.;v=_v;{ {
   }
 _current += inmda;
 _current += iampa;

} return _current;
}

static void nrn_cur(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; double _rhs, _v; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 _g = _nrn_current(_p, _ppvar, _thread, _nt, _v + .001);
 	{ _rhs = _nrn_current(_p, _ppvar, _thread, _nt, _v);
 	}
 _g = (_g - _rhs)/.001;
 _g *=  1.e2/(_nd_area);
 _rhs *= 1.e2/(_nd_area);
#if CACHEVEC
  if (use_cachevec) {
	VEC_RHS(_ni[_iml]) -= _rhs;
  }else
#endif
  {
	NODERHS(_nd) -= _rhs;
  }
 
}
 
}

static void nrn_jacob(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml];
#if CACHEVEC
  if (use_cachevec) {
	VEC_D(_ni[_iml]) += _g;
  }else
#endif
  {
     _nd = _ml->_nodelist[_iml];
	NODED(_nd) += _g;
  }
 
}
 
}

static void nrn_state(_NrnThread* _nt, _Memb_list* _ml, int _type) {
double* _p; Datum* _ppvar; Datum* _thread;
Node *_nd; double _v = 0.0; int* _ni; int _iml, _cntml;
#if CACHEVEC
    _ni = _ml->_nodeindices;
#endif
_cntml = _ml->_nodecount;
_thread = _ml->_thread;
for (_iml = 0; _iml < _cntml; ++_iml) {
 _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
 _nd = _ml->_nodelist[_iml];
#if CACHEVEC
  if (use_cachevec) {
    _v = VEC_V(_ni[_iml]);
  }else
#endif
  {
    _nd = _ml->_nodelist[_iml];
    _v = NODEV(_nd);
  }
 v=_v;
{
 {   release(_p, _ppvar, _thread, _nt);
  }}}

}

static void terminal(){}

static void _initlists(){
 double _x; double* _p = &_x;
 int _i; static int _first = 1;
  if (!_first) return;
 _slist1[0] = &(r_nmda) - _p;  _dlist1[0] = &(Dr_nmda) - _p;
 _slist1[1] = &(r_ampa) - _p;  _dlist1[1] = &(Dr_ampa) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/gjgpb9/LargeScaleBLA/components/mechanisms/modfiles/shock2pyr.mod";
static const char* nmodl_file_text = 
  ":Shock to Pyramidal Cells AMPA+NMDA with local Ca2+ pool\n"
  "\n"
  "NEURON {\n"
  "	POINT_PROCESS shock2pyr\n"
  "	NONSPECIFIC_CURRENT inmda, iampa\n"
  "	RANGE initW\n"
  "	RANGE Cdur_nmda, AlphaTmax_nmda, Beta_nmda, Erev_nmda, gbar_nmda, W_nmda, on_nmda, g_nmda\n"
  "	RANGE Cdur_ampa, AlphaTmax_ampa, Beta_ampa, Erev_ampa, gbar_ampa, W_ampa, on_ampa, g_ampa\n"
  "	RANGE pregid,postgid\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mV) = (millivolt)\n"
  "        (nA) = (nanoamp)\n"
  "	(uS) = (microsiemens)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "	initW = 10 : 15 : 12 : 9\n"
  "\n"
  "	Cdur_nmda = 16.7650 (ms)\n"
  "	AlphaTmax_nmda = .2659 (/ms)\n"
  "	Beta_nmda = 0.008 (/ms)\n"
  "	Erev_nmda = 0 (mV)\n"
  "	gbar_nmda = .5e-3 (uS)\n"
  "\n"
  "	Cdur_ampa = 1.4210 (ms)\n"
  "	AlphaTmax_ampa = 3.8142 (/ms)\n"
  "	Beta_ampa = 0.1429 (/ms)\n"
  "	Erev_ampa = 0 (mV)\n"
  "	gbar_ampa = 1e-3 (uS)\n"
  "}\n"
  "\n"
  "ASSIGNED {\n"
  "	v (mV)\n"
  "\n"
  "	inmda (nA)\n"
  "	g_nmda (uS)\n"
  "	on_nmda\n"
  "	W_nmda\n"
  "\n"
  "	iampa (nA)\n"
  "	g_ampa (uS)\n"
  "	on_ampa\n"
  "	W_ampa\n"
  "\n"
  "	t0 (ms)\n"
  "	\n"
  "	pregid\n"
  "	postgid\n"
  "}\n"
  "\n"
  "STATE { r_nmda r_ampa }\n"
  "\n"
  "INITIAL {\n"
  "	on_nmda = 0\n"
  "	r_nmda = 0\n"
  "	W_nmda = initW\n"
  "\n"
  "	on_ampa = 0\n"
  "	r_ampa = 0\n"
  "	W_ampa = initW\n"
  "\n"
  "	t0 = -1\n"
  "}\n"
  "\n"
  "BREAKPOINT {\n"
  "	SOLVE release METHOD cnexp\n"
  "}\n"
  "\n"
  "DERIVATIVE release {\n"
  "	if (t0>0) {\n"
  "		if (t-t0 < Cdur_nmda) {\n"
  "			on_nmda = 1\n"
  "		} else {\n"
  "			on_nmda = 0\n"
  "		}\n"
  "		if (t-t0 < Cdur_ampa) {\n"
  "			on_ampa = 1\n"
  "		} else {\n"
  "			on_ampa = 0\n"
  "		}\n"
  "	}\n"
  "	r_nmda' = AlphaTmax_nmda*on_nmda*(1-r_nmda)-Beta_nmda*r_nmda\n"
  "	r_ampa' = AlphaTmax_ampa*on_ampa*(1-r_ampa)-Beta_ampa*r_ampa\n"
  "\n"
  "	g_nmda = gbar_nmda*r_nmda\n"
  "	inmda = W_nmda*g_nmda*(v - Erev_nmda)*sfunc(v)\n"
  "\n"
  "	g_ampa = gbar_ampa*r_ampa\n"
  "	iampa = W_ampa*g_ampa*(v - Erev_ampa)\n"
  "}\n"
  "\n"
  "NET_RECEIVE(dummy_weight) {\n"
  "	t0 = t\n"
  "}\n"
  "\n"
  ":::::::::::: FUNCTIONs and PROCEDUREs ::::::::::::\n"
  "\n"
  "FUNCTION sfunc (v (mV)) {\n"
  "	UNITSOFF\n"
  "	sfunc = 1/(1+0.33*exp(-0.06*v))\n"
  "	UNITSON\n"
  "}\n"
  ;
#endif
