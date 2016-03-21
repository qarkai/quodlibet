# -*- coding: utf-8 -*-
# Copyright 2016 Christoph Reiter
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation

import ctypes
from ctypes import wintypes, cdll, windll

from .enum import enum


class GUID(ctypes.Structure):
    # https://msdn.microsoft.com/en-us/library/windows/desktop/
    #   aa373931%28v=vs.85%29.aspx

    _fields_ = [
        ("Data1", wintypes.DWORD),
        ("Data2", wintypes.WORD),
        ("Data3", wintypes.WORD),
        ("Data4", wintypes.BYTE * 8),
    ]

    def __init__(self, name=None):
        if name is not None:
            IIDFromString(str(name), ctypes.byref(self))

    def __str__(self):
        ptr = wintypes.LPOLESTR()
        StringFromIID(ctypes.byref(self), ctypes.byref(ptr))
        string = str(ptr.value)
        CoTaskMemFree(ptr)
        return string


LPGUID = ctypes.POINTER(GUID)
IID = GUID
LPIID = ctypes.POINTER(IID)
REFIID = ctypes.POINTER(IID)
CLSID = GUID
REFCLSID = ctypes.POINTER(CLSID)

DWORD = wintypes.DWORD

LPWIN32_FIND_DATAW = ctypes.POINTER(wintypes.WIN32_FIND_DATAW)

IIDFromString = windll.ole32.IIDFromString
IIDFromString.argtypes = [wintypes.LPCOLESTR, LPIID]
IIDFromString.restype = wintypes.HRESULT

StringFromIID = windll.ole32.StringFromIID
StringFromIID.argtypes = [REFIID, ctypes.POINTER(wintypes.LPOLESTR)]
StringFromIID.restype = wintypes.HRESULT

CoInitialize = windll.ole32.CoInitialize
CoInitialize.argtypes = [wintypes.LPVOID]
CoInitialize.restype = wintypes.HRESULT

LPDWORD = ctypes.POINTER(wintypes.DWORD)
REFKNOWNFOLDERID = ctypes.POINTER(GUID)

CLSCTX_INPROC_SERVER = 1

SetEnvironmentVariableW = ctypes.windll.kernel32.SetEnvironmentVariableW
SetEnvironmentVariableW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
SetEnvironmentVariableW.restype = ctypes.c_bool

GetEnvironmentStringsW = ctypes.windll.kernel32.GetEnvironmentStringsW
GetEnvironmentStringsW.argtypes = []
GetEnvironmentStringsW.restype = ctypes.c_void_p

FreeEnvironmentStringsW = ctypes.windll.kernel32.FreeEnvironmentStringsW
FreeEnvironmentStringsW.argtypes = [ctypes.c_void_p]
FreeEnvironmentStringsW.restype = ctypes.c_bool

SHGetFolderPathW = ctypes.windll.shell32.SHGetFolderPathW
SHGetFolderPathW.argtypes = [
    wintypes.HWND, ctypes.c_int, wintypes.HANDLE, wintypes.DWORD,
    wintypes.LPWSTR]
SHGetFolderPathW.restype = wintypes.HRESULT

SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
SHGetKnownFolderPath.argtypes = [
    REFKNOWNFOLDERID, wintypes.DWORD, wintypes.HANDLE,
    ctypes.POINTER(wintypes.c_wchar_p)]
SHGetKnownFolderPath.restype = wintypes.HRESULT

CoTaskMemFree = windll.ole32.CoTaskMemFree
CoTaskMemFree.argtypes = [ctypes.c_void_p]
CoTaskMemFree.restype = None

GetCommandLineW = cdll.kernel32.GetCommandLineW
GetCommandLineW.argtypes = []
GetCommandLineW.restype = wintypes.LPCWSTR

CommandLineToArgvW = windll.shell32.CommandLineToArgvW
CommandLineToArgvW.argtypes = [
    wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
CommandLineToArgvW.restype = ctypes.POINTER(wintypes.LPWSTR)

LocalFree = windll.kernel32.LocalFree
LocalFree.argtypes = [wintypes.HLOCAL]
LocalFree.restype = wintypes.HLOCAL

WaitNamedPipeW = windll.kernel32.WaitNamedPipeW
WaitNamedPipeW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD]
WaitNamedPipeW.restype = wintypes.BOOL


class SECURITY_ATTRIBUTES(ctypes.Structure):

    _fields_ = [
        ("nLength", wintypes.DWORD),
        ("lpSecurityDescriptor", wintypes.LPVOID),
        ("bInheritHandle", wintypes.BOOL),
    ]

LPSECURITY_ATTRIBUTES = ctypes.POINTER(SECURITY_ATTRIBUTES)
PSECURITY_ATTRIBUTES = LPSECURITY_ATTRIBUTES

CreateNamedPipeW = windll.kernel32.CreateNamedPipeW
CreateNamedPipeW.argtypes = [
    wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, wintypes.DWORD,
    wintypes.DWORD, wintypes.DWORD, wintypes.DWORD, LPSECURITY_ATTRIBUTES]
CreateNamedPipeW.restype = wintypes.HANDLE

LPOVERLAPPED = ctypes.c_void_p

PIPE_ACCEPT_REMOTE_CLIENTS = 0x00000000
PIPE_REJECT_REMOTE_CLIENTS = 0x00000008

PIPE_ACCESS_DUPLEX = 0x00000003
PIPE_ACCESS_INBOUND = 0x00000001
PIPE_ACCESS_OUTBOUND = 0x00000002

PIPE_TYPE_BYTE = 0x00000000
PIPE_TYPE_MESSAGE = 0x00000004

PIPE_READMODE_BYTE = 0x00000000
PIPE_READMODE_MESSAGE = 0x00000002

PIPE_WAIT = 0x00000000
PIPE_NOWAIT = 0x00000001

FILE_FLAG_FIRST_PIPE_INSTANCE = 0x00080000
FILE_FLAG_WRITE_THROUGH = 0x80000000
FILE_FLAG_OVERLAPPED = 0x40000000

PIPE_UNLIMITED_INSTANCES = 255

NMPWAIT_USE_DEFAULT_WAIT = 0x00000000
NMPWAIT_WAIT_FOREVER = 0xffffffff

ConnectNamedPipe = windll.kernel32.ConnectNamedPipe
ConnectNamedPipe.argtypes = [wintypes.HANDLE, LPOVERLAPPED]
ConnectNamedPipe.restype = wintypes.BOOL

DisconnectNamedPipe = windll.kernel32.DisconnectNamedPipe
DisconnectNamedPipe.argtypes = [wintypes.HANDLE]
DisconnectNamedPipe.restype = wintypes.BOOL

ReadFile = windll.kernel32.ReadFile
ReadFile.argtypes = [wintypes.HANDLE, wintypes.LPVOID, wintypes.DWORD,
                     LPDWORD, LPOVERLAPPED]
ReadFile.restype = wintypes.BOOL

CloseHandle = windll.kernel32.CloseHandle
CloseHandle.argtypes = [wintypes.HANDLE]
CloseHandle.restype = wintypes.BOOL

S_OK = wintypes.HRESULT(0).value
MAX_PATH = wintypes.MAX_PATH
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value


class COMMethod(object):

    def __init__(self, name, offset, restype, argtypes):
        self._name = name
        self._restype = restype
        self._offset = offset
        self._argtypes = argtypes

    def __get__(self, instance, owner):
        func = ctypes.WINFUNCTYPE(
            self._restype, *self._argtypes)(self._offset, self._name)

        def wrapper(self, *args, **kwargs):
            return func(self, *args, **kwargs)

        setattr(owner, self._name, wrapper)
        return getattr(instance or owner, self._name)


class COMInterface(type(ctypes.c_void_p)):

    def __new__(mcls, cls_name, bases, d):

        offset = 0
        for base in bases:
            for realbase in base.__mro__:
                offset += len(realbase.__dict__.get("_methods_", []))

        for i, args in enumerate(d.get("_methods_", [])):
            name = args[0]
            restype = args[1]
            argtypes = args[2:]
            m = COMMethod(name, offset + i, restype, argtypes)
            d[name] = m

        return type(ctypes.c_void_p).__new__(mcls, cls_name, bases, dict(d))


class IUnknown(ctypes.c_void_p):

    __metaclass__ = COMInterface

    IID = GUID("{00000001-0000-0000-c000-000000000046}")

    _methods_ = [
      ("QueryInterface", wintypes.HRESULT, LPGUID, wintypes.LPVOID),
      ("AddRef", wintypes.DWORD),
      ("Release", wintypes.DWORD),
    ]


LPUNKNOWN = ctypes.POINTER(IUnknown)

CoCreateInstance = windll.ole32.CoCreateInstance
CoCreateInstance.argtypes = [REFCLSID, LPUNKNOWN, wintypes.DWORD, REFIID,
                             wintypes.LPVOID]
CoCreateInstance.restype = wintypes.HRESULT


class IShellLinkW(IUnknown):

    IID = GUID("{000214F9-0000-0000-C000-000000000046}")

    _methods_ = [
        ("GetPath", wintypes.HRESULT, wintypes.LPWSTR, wintypes.INT,
         LPWIN32_FIND_DATAW, wintypes.DWORD),
    ]


class IPersist(IUnknown):

    IID = GUID("{0000010c-0000-0000-C000-000000000046}")

    _methods_ = [
        ("GetClassID", wintypes.HRESULT, LPGUID),
    ]


class IPersistFile(IPersist):

    IID = GUID("{0000010b-0000-0000-c000-000000000046}")

    _methods_ = [
        ("IsDirty", wintypes.HRESULT),
        ("Load", wintypes.HRESULT, wintypes.LPOLESTR, wintypes.DWORD),
    ]


CLSID_ShellLink = GUID("{00021401-0000-0000-C000-000000000046}")


@enum
class FOLDERID(str):
    LINKS = "{bfb9d5e0-c6a9-404c-b2b2-ae6db6af4968}"


@enum
class SHGFPType(int):
    CURRENT = 0
    DEFAULT = 1


@enum
class CSIDL(int):
    DESKTOP = 0x0000
    PERSONAL = 0x0005
    APPDATA = 0x001A
    MYMUSIC = 0x000d
    PROFILE = 0x0028


@enum
class CSIDLFlag(int):
    PER_USER_INIT = 0x0800
    NO_ALIAS = 0x1000
    DONT_UNEXPAND = 0x2000
    DONT_VERIFY = 0x4000
    CREATE = 0x8000
    MASK = 0xFF00


@enum
class KnownFolderFlag(long):
    SIMPLE_IDLIST = 0x00000100
    NOT_PARENT_RELATIVE = 0x00000200
    DEFAULT_PATH = 0x00000400
    INIT = 0x00000800
    NO_ALIAS = 0x00001000
    DONT_UNEXPAND = 0x00002000
    DONT_VERIFY = 0x00004000
    CREATE = 0x00008000
    NO_APPCONTAINER_REDIRECTION = 0x00010000
    ALIAS_ONLY = 0x80000000
