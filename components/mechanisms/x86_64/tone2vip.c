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
 
#define nrn_init _nrn_init__tone2vip
#define _nrn_initial _nrn_initial__tone2vip
#define nrn_cur _nrn_cur__tone2vip
#define _nrn_current _nrn_current__tone2vip
#define nrn_jacob _nrn_jacob__tone2vip
#define nrn_state _nrn_state__tone2vip
#define _net_receive _net_receive__tone2vip 
#define release release__tone2vip 
 
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
#define srcid _p[0]
#define destid _p[1]
#define Cdur_nmda _p[2]
#define AlphaTmax_nmda _p[3]
#define Beta_nmda _p[4]
#define Erev_nmda _p[5]
#define gbar_nmda _p[6]
#define Cdur_ampa _p[7]
#define AlphaTmax_ampa _p[8]
#define Beta_ampa _p[9]
#define Erev_ampa _p[10]
#define gbar_ampa _p[11]
#define Cainf _p[12]
#define pooldiam _p[13]
#define z _p[14]
#define tauCa _p[15]
#define P0n _p[16]
#define fCan _p[17]
#define P0a _p[18]
#define fCaa _p[19]
#define lambda1 _p[20]
#define lambda2 _p[21]
#define threshold1 _p[22]
#define threshold2 _p[23]
#define initW _p[24]
#define fmax _p[25]
#define fmin _p[26]
#define inmda _p[27]
#define g_nmda _p[28]
#define on_nmda _p[29]
#define W_nmda _p[30]
#define iampa _p[31]
#define g_ampa _p[32]
#define on_ampa _p[33]
#define W _p[34]
#define ICan _p[35]
#define ICaa _p[36]
#define Icatotal _p[37]
#define Wmax _p[38]
#define Wmin _p[39]
#define maxChange _p[40]
#define normW _p[41]
#define scaleW _p[42]
#define pregid _p[43]
#define postgid _p[44]
#define r_nmda _p[45]
#define r_ampa _p[46]
#define capoolcon _p[47]
#define eca _p[48]
#define t0 _p[49]
#define Afactor _p[50]
#define dW_ampa _p[51]
#define Dr_nmda _p[52]
#define Dr_ampa _p[53]
#define Dcapoolcon _p[54]
#define v _p[55]
#define _g _p[56]
#define _tsav _p[57]
#define _nd_area  *_ppvar[0]._pval
#define _ion_eca	*_ppvar[2]._pval
 
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
 static double _hoc_GAP1();
 static double _hoc_eta();
 static double _hoc_omega();
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
 "GAP1", _hoc_GAP1,
 "eta", _hoc_eta,
 "omega", _hoc_omega,
 "sfunc", _hoc_sfunc,
 0, 0
};
#define GAP1 GAP1_tone2vip
#define eta eta_tone2vip
#define omega omega_tone2vip
#define sfunc sfunc_tone2vip
 extern double GAP1( _threadargsprotocomma_ double , double );
 extern double eta( _threadargsprotocomma_ double );
 extern double omega( _threadargsprotocomma_ double , double , double );
 extern double sfunc( _threadargsprotocomma_ double );
 /* declare global and static user variables */
#define GAPstop1 GAPstop1_tone2vip
 double GAPstop1 = 196000;
#define GAPstart1 GAPstart1_tone2vip
 double GAPstart1 = 96000;
 /* some parameters have upper and lower limits */
 static HocParmLimits _hoc_parm_limits[] = {
 0,0,0
};
 static HocParmUnits _hoc_parm_units[] = {
 "srcid", "1",
 "destid", "1",
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
 "Cainf", "mM",
 "pooldiam", "micrometer",
 "tauCa", "ms",
 "inmda", "nA",
 "g_nmda", "uS",
 "iampa", "nA",
 "g_ampa", "uS",
 "ICan", "mA",
 "ICaa", "mA",
 "Icatotal", "mA",
 0,0
};
 static double capoolcon0 = 0;
 static double delta_t = 0.01;
 static double r_ampa0 = 0;
 static double r_nmda0 = 0;
 /* connect global user variables to hoc */
 static DoubScal hoc_scdoub[] = {
 "GAPstart1_tone2vip", &GAPstart1_tone2vip,
 "GAPstop1_tone2vip", &GAPstop1_tone2vip,
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
 
#define _cvode_ieq _ppvar[3]._i
 static void _ode_matsol_instance1(_threadargsproto_);
 /* connect range variables in _p that hoc is supposed to know about */
 static const char *_mechanism[] = {
 "7.7.0",
"tone2vip",
 "srcid",
 "destid",
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
 "Cainf",
 "pooldiam",
 "z",
 "tauCa",
 "P0n",
 "fCan",
 "P0a",
 "fCaa",
 "lambda1",
 "lambda2",
 "threshold1",
 "threshold2",
 "initW",
 "fmax",
 "fmin",
 0,
 "inmda",
 "g_nmda",
 "on_nmda",
 "W_nmda",
 "iampa",
 "g_ampa",
 "on_ampa",
 "W",
 "ICan",
 "ICaa",
 "Icatotal",
 "Wmax",
 "Wmin",
 "maxChange",
 "normW",
 "scaleW",
 "pregid",
 "postgid",
 0,
 "r_nmda",
 "r_ampa",
 "capoolcon",
 0,
 0};
 static Symbol* _ca_sym;
 
extern Prop* need_memb(Symbol*);

static void nrn_alloc(Prop* _prop) {
	Prop *prop_ion;
	double *_p; Datum *_ppvar;
  if (nrn_point_prop_) {
	_prop->_alloc_seq = nrn_point_prop_->_alloc_seq;
	_p = nrn_point_prop_->param;
	_ppvar = nrn_point_prop_->dparam;
 }else{
 	_p = nrn_prop_data_alloc(_mechtype, 58, _prop);
 	/*initialize range parameters*/
 	srcid = -1;
 	destid = -1;
 	Cdur_nmda = 16.765;
 	AlphaTmax_nmda = 0.2659;
 	Beta_nmda = 0.008;
 	Erev_nmda = 0;
 	gbar_nmda = 0.0005;
 	Cdur_ampa = 0.713;
 	AlphaTmax_ampa = 10.1571;
 	Beta_ampa = 0.4167;
 	Erev_ampa = 0;
 	gbar_ampa = 0.001;
 	Cainf = 5e-05;
 	pooldiam = 1.8172;
 	z = 2;
 	tauCa = 50;
 	P0n = 0.015;
 	fCan = 0.024;
 	P0a = 0.0015;
 	fCaa = 0.024;
 	lambda1 = 3;
 	lambda2 = 0.01;
 	threshold1 = 0.45;
 	threshold2 = 0.5;
 	initW = 4.5;
 	fmax = 4.3;
 	fmin = 0.8;
  }
 	_prop->param = _p;
 	_prop->param_size = 58;
  if (!nrn_point_prop_) {
 	_ppvar = nrn_prop_datum_alloc(_mechtype, 4, _prop);
  }
 	_prop->dparam = _ppvar;
 	/*connect ionic variables to this model*/
 prop_ion = need_memb(_ca_sym);
 nrn_promote(prop_ion, 0, 1);
 	_ppvar[2]._pval = &prop_ion->param[0]; /* eca */
 
}
 static void _initlists();
  /* some states have an absolute tolerance */
 static Symbol** _atollist;
 static HocStateTolerance _hoc_state_tol[] = {
 0,0
};
 static void _net_receive(Point_process*, double*, double);
 static void _update_ion_pointer(Datum*);
 extern Symbol* hoc_lookup(const char*);
extern void _nrn_thread_reg(int, int, void(*)(Datum*));
extern void _nrn_thread_table_reg(int, void(*)(double*, Datum*, Datum*, _NrnThread*, int));
extern void hoc_register_tolerance(int, HocStateTolerance*, Symbol***);
extern void _cvode_abstol( Symbol**, double*, int);

 void _tone2vip_reg() {
	int _vectorized = 1;
  _initlists();
 	ion_reg("ca", -10000.);
 	_ca_sym = hoc_lookup("ca_ion");
 	_pointtype = point_register_mech(_mechanism,
	 nrn_alloc,nrn_cur, nrn_jacob, nrn_state, nrn_init,
	 hoc_nrnpointerindex, 1,
	 _hoc_create_pnt, _hoc_destroy_pnt, _member_func);
 _mechtype = nrn_get_mechtype(_mechanism[1]);
     _nrn_setdata_reg(_mechtype, _setdata);
     _nrn_thread_reg(_mechtype, 2, _update_ion_pointer);
 #if NMODL_TEXT
  hoc_reg_nmodl_text(_mechtype, nmodl_file_text);
  hoc_reg_nmodl_filename(_mechtype, nmodl_filename);
#endif
  hoc_register_prop_size(_mechtype, 58, 4);
  hoc_register_dparam_semantics(_mechtype, 0, "area");
  hoc_register_dparam_semantics(_mechtype, 1, "pntproc");
  hoc_register_dparam_semantics(_mechtype, 2, "ca_ion");
  hoc_register_dparam_semantics(_mechtype, 3, "cvodeieq");
 	hoc_register_cvode(_mechtype, _ode_count, _ode_map, _ode_spec, _ode_matsol);
 	hoc_register_tolerance(_mechtype, _hoc_state_tol, &_atollist);
 pnt_receive[_mechtype] = _net_receive;
 pnt_receive_size[_mechtype] = 1;
 	hoc_register_var(hoc_scdoub, hoc_vdoub, hoc_intfunc);
 	ivoc_help("help ?1 tone2vip /home/gjgpb9/LargeScaleBLA/components/mechanisms/x86_64/tone2vip.mod\n");
 hoc_register_limits(_mechtype, _hoc_parm_limits);
 hoc_register_units(_mechtype, _hoc_parm_units);
 }
 static double FARADAY = 96485.0;
 static double pi = 3.141592;
static int _reset;
static char *modelname = "";

static int error;
static int _ninits = 0;
static int _match_recurse=1;
static void _modl_cleanup(){ _match_recurse=1;}
 
static int _ode_spec1(_threadargsproto_);
/*static int _ode_matsol1(_threadargsproto_);*/
 static int _slist1[3], _dlist1[3];
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
   dW_ampa = eta ( _threadargscomma_ capoolcon ) * ( lambda1 * omega ( _threadargscomma_ capoolcon , threshold1 , threshold2 ) - lambda2 * GAP1 ( _threadargscomma_ GAPstart1 , GAPstop1 ) * W ) * dt ;
   if ( fabs ( dW_ampa ) > maxChange ) {
     if ( dW_ampa < 0.0 ) {
       dW_ampa = - 1.0 * maxChange ;
       }
     else {
       dW_ampa = maxChange ;
       }
     }
   g_nmda = gbar_nmda * r_nmda ;
   inmda = W_nmda * g_nmda * ( v - Erev_nmda ) * sfunc ( _threadargscomma_ v ) ;
   g_ampa = gbar_ampa * r_ampa ;
   iampa = W * g_ampa * ( v - Erev_ampa ) ;
   ICan = P0n * g_nmda * ( v - eca ) * sfunc ( _threadargscomma_ v ) ;
   ICaa = P0a * W * g_ampa * ( v - eca ) / initW ;
   Icatotal = ICan + ICaa ;
   Dcapoolcon = - fCan * Afactor * Icatotal + ( Cainf - capoolcon ) / tauCa ;
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
 dW_ampa = eta ( _threadargscomma_ capoolcon ) * ( lambda1 * omega ( _threadargscomma_ capoolcon , threshold1 , threshold2 ) - lambda2 * GAP1 ( _threadargscomma_ GAPstart1 , GAPstop1 ) * W ) * dt ;
 if ( fabs ( dW_ampa ) > maxChange ) {
   if ( dW_ampa < 0.0 ) {
     dW_ampa = - 1.0 * maxChange ;
     }
   else {
     dW_ampa = maxChange ;
     }
   }
 g_nmda = gbar_nmda * r_nmda ;
 inmda = W_nmda * g_nmda * ( v - Erev_nmda ) * sfunc ( _threadargscomma_ v ) ;
 g_ampa = gbar_ampa * r_ampa ;
 iampa = W * g_ampa * ( v - Erev_ampa ) ;
 ICan = P0n * g_nmda * ( v - eca ) * sfunc ( _threadargscomma_ v ) ;
 ICaa = P0a * W * g_ampa * ( v - eca ) / initW ;
 Icatotal = ICan + ICaa ;
 Dcapoolcon = Dcapoolcon  / (1. - dt*( ( ( ( - 1.0 ) ) ) / tauCa )) ;
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
   dW_ampa = eta ( _threadargscomma_ capoolcon ) * ( lambda1 * omega ( _threadargscomma_ capoolcon , threshold1 , threshold2 ) - lambda2 * GAP1 ( _threadargscomma_ GAPstart1 , GAPstop1 ) * W ) * dt ;
   if ( fabs ( dW_ampa ) > maxChange ) {
     if ( dW_ampa < 0.0 ) {
       dW_ampa = - 1.0 * maxChange ;
       }
     else {
       dW_ampa = maxChange ;
       }
     }
   g_nmda = gbar_nmda * r_nmda ;
   inmda = W_nmda * g_nmda * ( v - Erev_nmda ) * sfunc ( _threadargscomma_ v ) ;
   g_ampa = gbar_ampa * r_ampa ;
   iampa = W * g_ampa * ( v - Erev_ampa ) ;
   ICan = P0n * g_nmda * ( v - eca ) * sfunc ( _threadargscomma_ v ) ;
   ICaa = P0a * W * g_ampa * ( v - eca ) / initW ;
   Icatotal = ICan + ICaa ;
    capoolcon = capoolcon + (1. - exp(dt*(( ( ( - 1.0 ) ) ) / tauCa)))*(- ( ( ( - fCan )*( Afactor ) )*( Icatotal ) + ( ( Cainf ) ) / tauCa ) / ( ( ( ( - 1.0 ) ) ) / tauCa ) - capoolcon) ;
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
 
double eta ( _threadargsprotocomma_ double _lCani ) {
   double _leta;
 double _ltaulearn , _lP1 , _lP2 , _lP4 , _lCacon ;
 _lP1 = 0.1 ;
   _lP2 = _lP1 * 1e-4 ;
   _lP4 = 1.0 ;
   _lCacon = _lCani * 1e3 ;
   _ltaulearn = _lP1 / ( _lP2 + _lCacon * _lCacon * _lCacon ) + _lP4 ;
   _leta = 1.0 / _ltaulearn * 0.001 ;
   
return _leta;
 }
 
static double _hoc_eta(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  eta ( _p, _ppvar, _thread, _nt, *getarg(1) );
 return(_r);
}
 
double omega ( _threadargsprotocomma_ double _lCani , double _lthreshold1 , double _lthreshold2 ) {
   double _lomega;
 double _lr , _lmid , _lCacon ;
 _lCacon = _lCani * 1e3 ;
   _lr = ( _lthreshold2 - _lthreshold1 ) / 2.0 ;
   _lmid = ( _lthreshold1 + _lthreshold2 ) / 2.0 ;
   if ( _lCacon <= _lthreshold1 ) {
     _lomega = 0.0 ;
     }
   else if ( _lCacon >= _lthreshold2 ) {
     _lomega = 1.0 / ( 1.0 + 50.0 * exp ( - 50.0 * ( _lCacon - _lthreshold2 ) ) ) ;
     }
   else {
     _lomega = - sqrt ( _lr * _lr - ( _lCacon - _lmid ) * ( _lCacon - _lmid ) ) ;
     }
   
return _lomega;
 }
 
static double _hoc_omega(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  omega ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) , *getarg(3) );
 return(_r);
}
 
double GAP1 ( _threadargsprotocomma_ double _lGAPstart1 , double _lGAPstop1 ) {
   double _lGAP1;
 double _ls ;
 if ( t <= _lGAPstart1 ) {
     _lGAP1 = 1.0 ;
     }
   else if ( t >= _lGAPstart1  && t <= _lGAPstop1 ) {
     _lGAP1 = 1.0 ;
     }
   else {
     _lGAP1 = 1.0 ;
     }
   
return _lGAP1;
 }
 
static double _hoc_GAP1(void* _vptr) {
 double _r;
   double* _p; Datum* _ppvar; Datum* _thread; _NrnThread* _nt;
   _p = ((Point_process*)_vptr)->_prop->param;
  _ppvar = ((Point_process*)_vptr)->_prop->dparam;
  _thread = _extcall_thread;
  _nt = (_NrnThread*)((Point_process*)_vptr)->_vnt;
 _r =  GAP1 ( _p, _ppvar, _thread, _nt, *getarg(1) , *getarg(2) );
 return(_r);
}
 
static int _ode_count(int _type){ return 3;}
 
static void _ode_spec(_NrnThread* _nt, _Memb_list* _ml, int _type) {
   double* _p; Datum* _ppvar; Datum* _thread;
   Node* _nd; double _v; int _iml, _cntml;
  _cntml = _ml->_nodecount;
  _thread = _ml->_thread;
  for (_iml = 0; _iml < _cntml; ++_iml) {
    _p = _ml->_data[_iml]; _ppvar = _ml->_pdata[_iml];
    _nd = _ml->_nodelist[_iml];
    v = NODEV(_nd);
  eca = _ion_eca;
     _ode_spec1 (_p, _ppvar, _thread, _nt);
 }}
 
static void _ode_map(int _ieq, double** _pv, double** _pvdot, double* _pp, Datum* _ppd, double* _atol, int _type) { 
	double* _p; Datum* _ppvar;
 	int _i; _p = _pp; _ppvar = _ppd;
	_cvode_ieq = _ieq;
	for (_i=0; _i < 3; ++_i) {
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
  eca = _ion_eca;
 _ode_matsol_instance1(_threadargs_);
 }}
 extern void nrn_update_ion_pointer(Symbol*, Datum*, int, int);
 static void _update_ion_pointer(Datum* _ppvar) {
   nrn_update_ion_pointer(_ca_sym, _ppvar, 2, 0);
 }

static void initmodel(double* _p, Datum* _ppvar, Datum* _thread, _NrnThread* _nt) {
  int _i; double _save;{
  capoolcon = capoolcon0;
  r_ampa = r_ampa0;
  r_nmda = r_nmda0;
 {
   on_nmda = 0.0 ;
   r_nmda = 0.0 ;
   W_nmda = initW ;
   on_ampa = 0.0 ;
   r_ampa = 0.0 ;
   W = initW ;
   t0 = - 1.0 ;
   Wmax = fmax * initW ;
   Wmin = fmin * initW ;
   maxChange = ( Wmax - Wmin ) / 10.0 ;
   dW_ampa = 0.0 ;
   capoolcon = Cainf ;
   Afactor = 1.0 / ( z * FARADAY * 4.0 / 3.0 * pi * pow( ( pooldiam / 2.0 ) , 3.0 ) ) * ( 1e6 ) ;
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
  eca = _ion_eca;
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
  eca = _ion_eca;
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
  eca = _ion_eca;
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
 _slist1[2] = &(capoolcon) - _p;  _dlist1[2] = &(Dcapoolcon) - _p;
_first = 0;
}

#if defined(__cplusplus)
} /* extern "C" */
#endif

#if NMODL_TEXT
static const char* nmodl_filename = "/home/gjgpb9/LargeScaleBLA/components/mechanisms/modfiles/tone2vip.mod";
static const char* nmodl_file_text = 
  ":Tone to Interneuron Cells AMPA+NMDA with local Ca2+ pool\n"
  ":NON-Plastic\n"
  "\n"
  "NEURON {\n"
  "	POINT_PROCESS tone2vip\n"
  "	USEION ca READ eca	\n"
  "	NONSPECIFIC_CURRENT inmda, iampa\n"
  "	RANGE initW\n"
  "	RANGE Cdur_nmda, AlphaTmax_nmda, Beta_nmda, Erev_nmda, gbar_nmda, W_nmda, on_nmda, g_nmda\n"
  "	RANGE Cdur_ampa, AlphaTmax_ampa, Beta_ampa, Erev_ampa, gbar_ampa, W, on_ampa, g_ampa\n"
  "	RANGE eca, ICan, P0n, fCan, tauCa, Icatotal\n"
  "	RANGE ICaa, P0a, fCaa\n"
  "	RANGE Cainf, pooldiam, z\n"
  "	RANGE lambda1, lambda2, threshold1, threshold2\n"
  "	RANGE fmax, fmin, Wmax, Wmin, maxChange, normW, scaleW, srcid, destid\n"
  "	RANGE pregid,postgid\n"
  "}\n"
  "\n"
  "UNITS {\n"
  "	(mV) = (millivolt)\n"
  "        (nA) = (nanoamp)\n"
  "	(uS) = (microsiemens)\n"
  "	FARADAY = 96485 (coul)\n"
  "	pi = 3.141592 (1)\n"
  "}\n"
  "\n"
  "PARAMETER {\n"
  "\n"
  "	srcid = -1 (1)\n"
  "	destid = -1 (1)\n"
  "\n"
  "	Cdur_nmda = 16.7650 (ms)\n"
  "	AlphaTmax_nmda = .2659 (/ms)\n"
  "	Beta_nmda = 0.008 (/ms)\n"
  "	Erev_nmda = 0 (mV)\n"
  "	gbar_nmda = .5e-3 (uS)\n"
  "\n"
  "	Cdur_ampa = 0.713 (ms)\n"
  "	AlphaTmax_ampa = 10.1571 (/ms)\n"
  "	Beta_ampa = 0.4167 (/ms)\n"
  "	Erev_ampa = 0 (mV)\n"
  "	gbar_ampa = 1e-3 (uS)\n"
  "\n"
  "	eca = 120\n"
  "\n"
  "	Cainf = 50e-6 (mM)\n"
  "	pooldiam =  1.8172 (micrometer)\n"
  "	z = 2\n"
  "\n"
  "	tauCa = 50 (ms)\n"
  "	P0n = .015\n"
  "	fCan = .024\n"
  "	\n"
  "	P0a = .0015 : .001\n"
  "	fCaa = .024\n"
  "	\n"
  "	lambda1 = 3 : 4 : 3 : 4 : 5 : 7 : 10 \n"
  "	lambda2 = 0.01 \n"
  "	threshold1 = 0.45 : 0.5 : 0.55 : .4 : 0.35\n"
  "	threshold2 = 0.50 : 0.55 : 0.6 : 0.45 : 0.4\n"
  "	\n"
  "	initW = 4.5 : 6 : 8 : 7.5 : 6 : 5 : 4 : 5 : 4 : 3 : 4	\n"
  "	fmax = 4.3 : 3.8 : 4 : 3\n"
  "	fmin = .8		\n"
  "	\n"
  "	GAPstart1 = 96000\n"
  "	GAPstop1 = 196000		\n"
  "	\n"
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
  "	W\n"
  "\n"
  "	t0 (ms)\n"
  "\n"
  "	ICan (mA)\n"
  "	ICaa (mA)\n"
  "	Afactor	(mM/ms/nA)\n"
  "	Icatotal (mA)\n"
  "\n"
  "	dW_ampa\n"
  "	Wmax\n"
  "	Wmin\n"
  "	maxChange\n"
  "	normW\n"
  "	scaleW\n"
  "	\n"
  "	pregid\n"
  "	postgid\n"
  "}\n"
  "\n"
  "STATE { r_nmda r_ampa capoolcon }\n"
  "\n"
  "INITIAL {\n"
  "	on_nmda = 0\n"
  "	r_nmda = 0\n"
  "	W_nmda = initW\n"
  "\n"
  "	on_ampa = 0\n"
  "	r_ampa = 0\n"
  "	W = initW\n"
  "\n"
  "	t0 = -1\n"
  "\n"
  "	Wmax = fmax*initW\n"
  "	Wmin = fmin*initW\n"
  "	maxChange = (Wmax-Wmin)/10\n"
  "	dW_ampa = 0\n"
  "\n"
  "	capoolcon = Cainf\n"
  "	Afactor	= 1/(z*FARADAY*4/3*pi*(pooldiam/2)^3)*(1e6)\n"
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
  "	dW_ampa = eta(capoolcon)*(lambda1*omega(capoolcon, threshold1, threshold2)-lambda2*GAP1(GAPstart1, GAPstop1)*W)*dt\n"
  "\n"
  "	: Limit for extreme large weight changes\n"
  "	if (fabs(dW_ampa) > maxChange) {\n"
  "		if (dW_ampa < 0) {\n"
  "			dW_ampa = -1*maxChange\n"
  "		} else {\n"
  "			dW_ampa = maxChange\n"
  "		}\n"
  "	}\n"
  "\n"
  "	:Normalize the weight change\n"
  "	:normW = (W-Wmin)/(Wmax-Wmin)\n"
  "	:if (dW_ampa < 0) {\n"
  "	:	scaleW = sqrt(fabs(normW))\n"
  "	:} else {\n"
  "	:	scaleW = sqrt(fabs(1.0-normW))\n"
  "	:}\n"
  "\n"
  "	:W = W + dW_ampa*scaleW\n"
  "	\n"
  "	:Weight value limits\n"
  "	:if (W > Wmax) { \n"
  "	:	W = Wmax\n"
  "	:} else if (W < Wmin) {\n"
  " 	:	W = Wmin\n"
  "	:}\n"
  "\n"
  "	g_nmda = gbar_nmda*r_nmda\n"
  "	inmda = W_nmda*g_nmda*(v - Erev_nmda)*sfunc(v)\n"
  "\n"
  "	g_ampa = gbar_ampa*r_ampa\n"
  "	iampa = W*g_ampa*(v - Erev_ampa)\n"
  "\n"
  "	ICan = P0n*g_nmda*(v - eca)*sfunc(v)\n"
  "	ICaa = P0a*W*g_ampa*(v-eca)/initW	\n"
  "	Icatotal = ICan + ICaa\n"
  "	capoolcon'= -fCan*Afactor*Icatotal + (Cainf-capoolcon)/tauCa\n"
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
  "\n"
  "FUNCTION eta(Cani (mM)) {\n"
  "	LOCAL taulearn, P1, P2, P4, Cacon\n"
  "	P1 = 0.1\n"
  "	P2 = P1*1e-4\n"
  "	P4 = 1\n"
  "	Cacon = Cani*1e3\n"
  "	taulearn = P1/(P2+Cacon*Cacon*Cacon)+P4\n"
  "	eta = 1/taulearn*0.001\n"
  "}\n"
  "\n"
  "FUNCTION omega(Cani (mM), threshold1 (uM), threshold2 (uM)) {\n"
  "	LOCAL r, mid, Cacon\n"
  "	Cacon = Cani*1e3\n"
  "	r = (threshold2-threshold1)/2\n"
  "	mid = (threshold1+threshold2)/2\n"
  "	if (Cacon <= threshold1) { omega = 0}\n"
  "	else if (Cacon >= threshold2) {	omega = 1/(1+50*exp(-50*(Cacon-threshold2)))}\n"
  "	else {omega = -sqrt(r*r-(Cacon-mid)*(Cacon-mid))}\n"
  "}\n"
  "FUNCTION GAP1(GAPstart1 (ms), GAPstop1 (ms)) {\n"
  "	LOCAL s\n"
  "	if (t <= GAPstart1) { GAP1 = 1}\n"
  "	else if (t >= GAPstart1 && t <= GAPstop1) {GAP1 = 1}					: During the Gap, apply lamda2*2\n"
  "	else  {	GAP1 = 1}\n"
  "}\n"
  "\n"
  "\n"
  "\n"
  "\n"
  "\n"
  ;
#endif
